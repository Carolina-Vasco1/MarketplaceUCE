from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import SalesReport, AnalyticsData, UserReport

class ReportingService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_sales_reports(self, seller_id: str, period: str = "monthly", months: int = 12) -> List[SalesReport]:
        """Get sales reports for a seller"""
        reports = self.db.query(SalesReport).filter(
            SalesReport.seller_id == seller_id,
            SalesReport.period == period
        ).limit(months).all()
        return reports
    
    def get_sales_summary(self, seller_id: str):
        """Get sales summary for a seller"""
        reports = self.db.query(SalesReport).filter(
            SalesReport.seller_id == seller_id
        ).all()
        
        total_sales = sum(r.total_sales for r in reports)
        total_orders = sum(r.total_orders for r in reports)
        total_revenue = sum(r.total_revenue for r in reports)
        
        return {
            "seller_id": seller_id,
            "total_sales": total_sales,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "report_count": len(reports)
        }
    
    def get_sales_metrics(self, seller_id: str, start_date: str = None, end_date: str = None):
        """Get sales metrics for a seller"""
        query = self.db.query(SalesReport).filter(SalesReport.seller_id == seller_id)
        
        if start_date:
            query = query.filter(SalesReport.created_at >= start_date)
        if end_date:
            query = query.filter(SalesReport.created_at <= end_date)
        
        reports = query.all()
        
        return {
            "seller_id": seller_id,
            "period": f"{start_date} to {end_date}",
            "total_orders": sum(r.total_orders for r in reports),
            "total_revenue": sum(r.total_revenue for r in reports),
            "avg_order_value": sum(r.avg_order_value for r in reports) / len(reports) if reports else 0
        }
    
    def get_platform_summary(self):
        """Get overall platform sales summary"""
        all_reports = self.db.query(SalesReport).all()
        
        return {
            "total_sales": sum(r.total_sales for r in all_reports),
            "total_orders": sum(r.total_orders for r in all_reports),
            "total_revenue": sum(r.total_revenue for r in all_reports),
            "active_sellers": len(set(r.seller_id for r in all_reports))
        }
    
    def get_dashboard_analytics(self, period: str = "monthly"):
        """Get analytics dashboard data"""
        analytics = self.db.query(AnalyticsData).filter(
            AnalyticsData.dimension == period
        ).all()
        
        return {
            "period": period,
            "metrics": [
                {
                    "type": a.metric_type,
                    "value": a.value,
                    "timestamp": a.created_at
                }
                for a in analytics
            ]
        }
