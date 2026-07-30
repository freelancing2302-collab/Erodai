"""
Background task scheduler for automatic encroachment reports
Runs scheduled tasks to send reports automatically
"""
import asyncio
from datetime import datetime, time
import logging
from app.core.database import SessionLocal
from app.models.water_body import User, WaterBody
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class ReportScheduler:
<<<<<<< HEAD
    """Handles scheduled sending of encroachment reports"""
=======
    """Handles scheduled sending of encroachment alerts"""
>>>>>>> f977997 (Initial clean import of Erodai project)
    
    def __init__(self):
        self.running = False
        self.task = None
<<<<<<< HEAD
=======

    @staticmethod
    def _target_time() -> time:
        """Return the scheduled delivery time."""
        return time(9, 0, 0)
>>>>>>> f977997 (Initial clean import of Erodai project)
    
    async def start(self):
        """Start the scheduler"""
        self.running = True
        self.task = asyncio.create_task(self._run_scheduler())
<<<<<<< HEAD
        logger.info("📅 Encroachment report scheduler started")
=======
        logger.info("📅 Encroachment alert scheduler started")
>>>>>>> f977997 (Initial clean import of Erodai project)
    
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.task:
            self.task.cancel()
<<<<<<< HEAD
        logger.info("📅 Encroachment report scheduler stopped")
    
    async def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                # Check if it's time to send the report
                # Default: Send at 9:00 AM every day
                now = datetime.now()
                current_time = now.time()
                
                # Send report at 09:00 every day
                target_time = time(9, 0, 0)
                
                if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
                    logger.info("⏰ Scheduled time reached - sending encroachment reports")
                    await self._send_reports()
                    # Wait 60 seconds to avoid duplicate sends
                    await asyncio.sleep(60)
                else:
                    # Check every 5 minutes
=======
        logger.info("📅 Encroachment alert scheduler stopped")
    
    async def _run_scheduler(self):
        """Main scheduler loop"""
        self.running = True
        while self.running:
            try:
                now = datetime.now()
                current_time = now.time()
                target_time = self._target_time()
                
                if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
                    logger.info("⏰ Scheduled time reached - sending encroachment alerts")
                    await self._send_alerts()
                    await asyncio.sleep(60)
                else:
>>>>>>> f977997 (Initial clean import of Erodai project)
                    await asyncio.sleep(300)
                    
            except Exception as e:
                logger.error(f"Error in report scheduler: {str(e)}")
                await asyncio.sleep(300)
    
<<<<<<< HEAD
    @staticmethod
    async def _send_reports():
        """Send encroachment reports to all users"""
        db = SessionLocal()
        try:
            logger.info("🔍 Fetching encroached water bodies...")
            
            # Get encroached water bodies
            encroached_bodies = db.query(WaterBody).filter(WaterBody.is_encroached == True).all()
            
            if not encroached_bodies:
                logger.info("No encroached water bodies found")
                return
            
            # Format data
            water_bodies_data = []
            for wb in encroached_bodies:
                encroach_pct = wb.last_water_loss_percent or 0
                severity = 'CRITICAL' if encroach_pct >= 20 else 'HIGH'
                
                water_body = {
                    'name': wb.name or 'Unknown',
                    'type': wb.body_type or 'Unknown',
                    'description': wb.description or 'N/A',
                    'encroachment_percent': encroach_pct,
                    'water_level_percent': 100 - encroach_pct,
                    'area': wb.area_sq_km or 0,
                    'severity': severity,
                    'water_quality': 'Fair',
                    'nearby_population': f"{int(wb.urbanization_level * 100000)}" if wb.urbanization_level else '0',
                    'ndvi_index': '0.50',
                    'ndbi_index': '0.28',
                }
                water_bodies_data.append(water_body)
            
            logger.info(f"Found {len(water_bodies_data)} encroached water bodies")
            
            # Get active users
=======
    async def _send_alerts(self):
        """Send encroachment alert emails to all active users."""
        db = SessionLocal()
        try:
            logger.info("🔍 Fetching encroached water bodies for scheduled alerts...")
            
            encroached_bodies = db.query(WaterBody).filter(WaterBody.is_encroached == True).all()
            
            if not encroached_bodies:
                logger.info("No encroached water bodies found for scheduled alert delivery")
                return
            
>>>>>>> f977997 (Initial clean import of Erodai project)
            users = db.query(User).filter(User.is_active == True).all()
            
            if not users:
                logger.warning("No active users found")
                return
            
<<<<<<< HEAD
            logger.info(f"Sending report to {len(users)} users...")
            
            sent = 0
            failed = 0
            
            for user in users:
                try:
                    success = EmailService.send_encroachment_report(
                        recipient_email=user.email,
                        water_bodies_data=water_bodies_data
                    )
                    if success:
                        sent += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Error sending to {user.email}: {str(e)}")
                    failed += 1
            
            logger.info(f"📊 Report send completed: {sent} sent, {failed} failed")
            
        except Exception as e:
            logger.error(f"Error sending scheduled reports: {str(e)}")
        finally:
            db.close()

=======
            sent = 0
            failed = 0
            
            for water_body in encroached_bodies:
                try:
                    encroachment_details = {
                        "water_body_details": {
                            "name": water_body.name,
                            "body_type": water_body.body_type or "Unknown",
                            "area_sq_km": water_body.area_sq_km,
                            "location": water_body.location,
                            "alert_threshold": water_body.alert_threshold,
                            "urbanization_level": water_body.urbanization_level,
                            "is_seasonal": water_body.is_seasonal,
                            "last_monitored": water_body.last_monitored,
                            "encroached_at": water_body.encroached_at,
                        },
                        "name": water_body.name,
                        "type": water_body.body_type or "Unknown",
                        "area": water_body.area_sq_km,
                        "detected_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    }

                    stats = EmailService.send_encroachment_alert_to_active_users(
                        db=db,
                        water_body_name=water_body.name,
                        encroachment_details=encroachment_details,
                    )
                    sent += stats.get("sent", 0)
                    failed += stats.get("failed", 0)
                except Exception as e:
                    logger.error(f"Error sending alert for {water_body.name}: {str(e)}")
                    failed += 1
            
            logger.info(f"📊 Alert send completed: {sent} sent, {failed} failed")
            
        except Exception as e:
            logger.error(f"Error sending scheduled alerts: {str(e)}")
        finally:
            db.close()

    async def _send_reports(self):
        """Backward-compatible wrapper for the old report path."""
        await self._send_alerts()

>>>>>>> f977997 (Initial clean import of Erodai project)

# Global scheduler instance
scheduler = ReportScheduler()
