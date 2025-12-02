#from .database import get_db
from .models import AllowedDomain


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import AllowedDomain, Base
from .database import engine # This uses your existing engine
import os

# If running standalone (not inside Docker), use local DB URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/neighboride_db")

# Only needed if running this file directly (not imported)
if __name__ == "__main__":
    # Create engine and tables if they don't exist
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# List of 50+ real Charlotte-area companies & universities
CHARLOTTE_COMPANIES = [
    ("wellsfargo.com", "Wells Fargo"),
    ("bankofamerica.com", "Bank of America"),
    ("truist.com", "Truist"),
    ("lowes.com", "Lowe's"),
    ("duke-energy.com", "Duke Energy"),
    ("atriumhealth.org", "Atrium Health"),
    ("novanthealth.org", "Novant Health"),
    ("charlotte.edu", "UNC Charlotte"),
    ("davidson.edu", "Davidson College"),
    ("queens.edu", "Queens University of Charlotte"),
    ("jwu.edu", "Johnson & Wales Charlotte"),
    ("cpcc.edu", "Central Piedmont Community College"),
    ("tiaa.org", "TIAA"),
    ("honeywell.com", "Honeywell"),
    ("siemens.com", "Siemens"),
    ("redventures.com", "Red Ventures"),
    ("lendingtree.com", "LendingTree"),
    ("avidxchange.com", "AvidXchange"),
    ("passportinc.com", "Passport"),
    ("skookum.com", "Skookum"),
    ("ally.com", "Ally Financial"),
    ("electrolux.com", "Electrolux"),
    ("compassgroupcareers.com", "Compass Group"),
    ("sealedair.com", "Sealed Air"),
    ("xpo.com", "XPO Logistics"),
    ("domtar.com", "Domtar"),
    ("belk.com", "Belk"),
    ("familydollar.com", "Family Dollar"),
    ("dollartree.com", "Dollar Tree"),
    ("snyderlance.com", "Snyder's-Lance"),
    ("jeld-wen.com", "JELD-WEN"),
    ("curtisswright.com", "Curtiss-Wright"),
    ("spx.com", "SPX Corporation"),
    ("nucor.com", "Nucor"),
    ("continental-corporation.com", "Continental"),
    ("brighthousefinancial.com", "Brighthouse Financial"),
    ("extendedstay.com", "Extended Stay America"),
    ("sonicautomotive.com", "Sonic Automotive"),
    ("cato.org", "Cato Corporation"),
    ("carolina.rr.com", "Road Runner (Spectrum)"),
    ("windstream.com", "Windstream"),
    ("commscope.com", "CommScope"),
    ("inspirebrands.com", "Inspire Brands"),
    ("boingo.com", "Boingo Wireless"),
    ("premierinc.com", "Premier Inc."),
    ("areva.com", "Framatome"),
    ("bbt.com", "BB&T (legacy)"),
    ("sunbelt-rentals.com", "Sunbelt Rentals"),
    ("crescentcommunities.com", "Crescent Communities"),
    ("childressklein.com", "Childress Klein"),
]

def seed_domains():
    db = SessionLocal()
    try:
        print("Seeding 50+ Charlotte corporate domains...")

        for domain, company_name in CHARLOTTE_COMPANIES:
            # Skip if already exists
            exists = db.query(AllowedDomain).filter(AllowedDomain.domain == domain).first()
            if not exists:
                db_domain = AllowedDomain(
                    domain=domain,
                    company_name=company_name or domain.split(".")[0].title(),
                    is_active=True
                )
                db.add(db_domain)
                print(f"Added: {domain}")

        db.commit()
        print("All Charlotte corporate domains seeded successfully!")
        print("You can now register with emails like: john@wellsfargo.com")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

# Run automatically if executed directly
if __name__ == "__main__":
    seed_domains()