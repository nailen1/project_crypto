"""
Test PostgreSQL connection with safe password handling
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection with safe URL encoding"""
    
    print("🔗 Testing PostgreSQL connection...\n")
    
    # Build DATABASE_URL safely
    db_user = os.getenv('DB_USER', 'juneyoung')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'database_quant')
    
    # URL encode password to handle special characters
    encoded_password = quote_plus(db_password)
    
    # Build connection string
    database_url = f"postgresql+psycopg://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    
    # Debug output (hide password)
    safe_url = database_url.replace(encoded_password, '****')
    print(f"🔍 DATABASE_URL: {safe_url}")
    print(f"🔍 Database: {db_name}")
    print(f"🔍 User: {db_user}")
    print(f"🔍 Host: {db_host}:{db_port}\n")
    
    try:
        # Create engine
        engine = create_engine(
            database_url,
            echo=False,
            pool_pre_ping=True
        )
        
        # Test connection
        with engine.connect() as conn:
            # Check version
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected successfully!")
            print(f"📊 PostgreSQL version:")
            print(f"   {version[:80]}...\n")
            
            # Check database and user
            result = conn.execute(text("""
                SELECT current_database() as db, 
                       current_user as user,
                       current_schema() as schema;
            """))
            row = result.fetchone()
            print(f"🗄️  Current Database: {row[0]}")
            print(f"👤 Current User: {row[1]}")
            print(f"📂 Current Schema: {row[2]}\n")
            
            # Check schemas
            result = conn.execute(text("""
                SELECT schema_name 
                FROM information_schema.schemata
                WHERE schema_name NOT LIKE 'pg_%'
                AND schema_name != 'information_schema'
                ORDER BY schema_name;
            """))
            schemas = [row[0] for row in result]
            print(f"📋 Available schemas: {schemas}\n")
            
            # Check tables in quant schema
            result = conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'quant'
                ORDER BY tablename;
            """))
            tables = [row[0] for row in result]
            print(f"📊 Tables in 'quant' schema: {tables}\n")
            
            print("🎉 All tests passed!")
            
    except Exception as e:
        print(f"\n❌ Connection failed!")
        print(f"Error: {e}\n")
        print("🔍 Troubleshooting:")
        print("1. Check Docker: docker compose ps")
        print("2. Check database exists:")
        print(f"   docker exec -it quant-postgres psql -U {db_user} -l")
        print("3. Create database if missing:")
        print(f"   docker exec -it quant-postgres createdb -U {db_user} {db_name}")

if __name__ == "__main__":
    test_connection()
