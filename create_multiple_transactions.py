"""Script to create test data for the application."""

import os
import sys
from sqlmodel import Session

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.db import engine
from app.models import Customer, Transaction, Plan, CustomerPlan, StatusEnum
from app.core.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def create_test_data():
    """Create comprehensive test data."""
    logger.info("Starting test data creation...")
    
    with Session(engine) as session:
        try:
            # Create test customers
            customers_data = [
                {
                    "name": "Julio Martinez",
                    "description": "Estudiante permanente",
                    "email": "julio@example.com",
                    "age": 33,
                },
                {
                    "name": "Maria Rodriguez",
                    "description": "Profesional en tecnología",
                    "email": "maria@example.com",
                    "age": 28,
                },
                {
                    "name": "Carlos Mendez",
                    "description": "Empresario",
                    "email": "carlos@example.com",
                    "age": 45,
                },
            ]
            
            customers = []
            for customer_data in customers_data:
                customer = Customer(**customer_data)
                session.add(customer)
                customers.append(customer)
            
            session.commit()
            logger.info(f"Created {len(customers)} customers")
            
            # Refresh customers to get their IDs
            for customer in customers:
                session.refresh(customer)
            
            # Create test plans
            plans_data = [
                {
                    "name": "Basic Plan",
                    "description": "Basic features for individuals",
                    "price": 999,  # $9.99 in cents
                },
                {
                    "name": "Premium Plan", 
                    "description": "Advanced features for professionals",
                    "price": 2999,  # $29.99 in cents
                },
                {
                    "name": "Enterprise Plan",
                    "description": "Full features for businesses",
                    "price": 9999,  # $99.99 in cents
                },
            ]
            
            plans = []
            for plan_data in plans_data:
                plan = Plan(**plan_data)
                session.add(plan)
                plans.append(plan)
            
            session.commit()
            logger.info(f"Created {len(plans)} plans")
            
            # Refresh plans to get their IDs
            for plan in plans:
                session.refresh(plan)
            
            # Create customer-plan relationships
            customer_plans = [
                CustomerPlan(customer_id=customers[0].id, plan_id=plans[0].id, status=StatusEnum.active),
                CustomerPlan(customer_id=customers[1].id, plan_id=plans[1].id, status=StatusEnum.active),
                CustomerPlan(customer_id=customers[2].id, plan_id=plans[2].id, status=StatusEnum.active),
                CustomerPlan(customer_id=customers[0].id, plan_id=plans[1].id, status=StatusEnum.inactive),
            ]
            
            for customer_plan in customer_plans:
                session.add(customer_plan)
            
            session.commit()
            logger.info(f"Created {len(customer_plans)} customer-plan relationships")
            
            # Create test transactions
            transaction_count = 0
            for i, customer in enumerate(customers):
                # Create different numbers of transactions per customer
                num_transactions = 50 + (i * 25)  # 50, 75, 100 transactions
                
                for x in range(num_transactions):
                    transaction = Transaction(
                        customer_id=customer.id,
                        description=f"Test transaction #{x+1} for {customer.name}",
                        amount=100 + (x * 50),  # Varying amounts
                    )
                    session.add(transaction)
                    transaction_count += 1
            
            session.commit()
            logger.info(f"Created {transaction_count} transactions")
            
            # Print summary
            print("\n" + "="*50)
            print("TEST DATA CREATION SUMMARY")
            print("="*50)
            print(f"✅ Customers: {len(customers)}")
            print(f"✅ Plans: {len(plans)}")
            print(f"✅ Customer-Plan relationships: {len(customer_plans)}")
            print(f"✅ Transactions: {transaction_count}")
            print("\nCustomers created:")
            for customer in customers:
                print(f"  - {customer.name} (ID: {customer.id}, Email: {customer.email})")
            print("\nPlans created:")
            for plan in plans:
                print(f"  - {plan.name} (ID: {plan.id}, Price: ${plan.price/100:.2f})")
            print("\n" + "="*50)
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating test data: {e}")
            raise


if __name__ == "__main__":
    create_test_data()