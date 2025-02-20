import os
import socket
import psycopg2
from psycopg2._psycopg import parse_dsn
from psycopg2.extensions import connection
import logging
import traceback


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('db_connection')


def diagnose_connection(host, port):
    """Perform network diagnostics"""
    try:
        ip_addr = socket.gethostbyname(host)
        logger.info(f"DNS Resolution: {host} -> {ip_addr}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip_addr, port))
        sock.close()

        if result == 0:
            logger.info(f"Port {port} is open on {host}")
        else:
            logger.error(f"Port {port} is closed on {host} (error: {result})")
    except Exception as e:
        logger.error(f"Network diagnostic failed: {str(e)}")


def get_db_connection() -> connection:
    """Get database connection with enhanced logging and diagnostics"""
    try:
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        # Log masked URL
        masked_url = db_url.replace(db_url.split('@')[0].split(':')[-1], '****')
        logger.info(f"Attempting connection with URL: {masked_url}")

        # Parse connection parameters
        params = parse_dsn(db_url)
        logger.info(f"Host: {params.get('host')}, Port: {params.get('port', 5432)}, "
                    f"Database: {params.get('dbname')}, User: {params.get('user')}")

        # Register type adapters
        from psycopg2.extras import register_uuid
        register_uuid()

        # Run network diagnostics
        logger.info("Running network diagnostics...")
        diagnose_connection(params.get('host'), int(params.get('port', 5432)))

        # Update with required parameters
        params.update({
            # 'sslmode': 'require',
            'connect_timeout': 10,
            'application_name': 'my_app',
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
            'tcp_user_timeout': 10000,
            'options': '-c timezone=UTC'
        })

        logger.info("Attempting to establish database connection...")
        conn = psycopg2.connect(**params)

        # Test connection
        with conn.cursor() as cur:
            cur.execute('SELECT 1')
            logger.info("Database connection test successful")

        return conn

    except psycopg2.OperationalError as e:
        logger.error("Database connection failed!")
        logger.error(f"Error details: {str(e)}")
        logger.error(f"Error traceback: {traceback.format_exc()}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during connection: {str(e)}")
        logger.error(f"Error traceback: {traceback.format_exc()}")
        raise
