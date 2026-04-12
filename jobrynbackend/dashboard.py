from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

# Core Models
from account.models import User
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from billing.models import Invoice, PayrollRecord, Payment

# Social & Engagement
from posts.models import Post, Comment, Like
from stories.models import Stori, StoriLike, StoriView, StoriComment
from follows.models import Follow
from connections.models import Connection
from messages.models import Message
from newsletters.models import Newsletter, Subscriber

# Talent & Portfolio
from skills.models import Skill, UserSkill
from projects.models import Project
from certifications.models import Certification
from learning.models import Course, Enrollment

# Logistics
from meetings.models import Meeting
from notifications.models import Notification


def get_kpi_stats(request):
    """Real-time platform KPIs shown on admin dashboard."""
    last_30_days = timezone.now() - timedelta(days=30)

    total_revenue = Invoice.objects.filter(status='paid').aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    new_users = User.objects.filter(created_at__gte=last_30_days).count()
    new_jobs = Job.objects.filter(created_at__gte=last_30_days).count()

    return [
        {
            "title": _("Total Revenue (NPR)"),
            "metric": f"NPR {total_revenue:,.0f}",
            "footer": _("Paid invoices"),
        },
        {
            "title": _("Total Users"),
            "metric": str(User.objects.count()),
            "footer": f"+{new_users} this month",
        },
        {
            "title": _("Active Jobs"),
            "metric": str(Job.objects.filter(is_active=True).count()),
            "footer": f"+{new_jobs} new this month",
        },
        {
            "title": _("Companies"),
            "metric": str(Company.objects.count()),
            "footer": f"{Company.objects.filter(is_verified=True).count()} verified",
        },
        {
            "title": _("Total Applications"),
            "metric": str(Application.objects.count()),
            "footer": f"{Application.objects.filter(status='hired').count()} hired",
        },
        {
            "title": _("Courses"),
            "metric": str(Course.objects.filter(is_published=True).count()),
            "footer": f"{Enrollment.objects.count()} total enrollments",
        },
    ]


def get_hiring_chart_data(request):
    """Application funnel — last 6 months."""
    months_labels = []
    for i in range(5, -1, -1):
        d = timezone.now() - timedelta(days=i * 30)
        months_labels.append(d.strftime("%b %Y"))

    # Real aggregation by month — last 6 months
    from_date = timezone.now() - timedelta(days=180)
    apps_by_month = (
        Application.objects
        .filter(created_at__gte=from_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    hires_by_month = (
        Application.objects
        .filter(status='hired', hired_at__gte=from_date)
        .annotate(month=TruncMonth('hired_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    apps_map = {str(a['month'])[:7]: a['count'] for a in apps_by_month}
    hires_map = {str(h['month'])[:7]: h['count'] for h in hires_by_month}

    from_dates = [(timezone.now() - timedelta(days=i * 30)).strftime("%Y-%m") for i in range(5, -1, -1)]

    return {
        "labels": months_labels,
        "datasets": [
            {
                "label": _("Applications"),
                "data": [apps_map.get(m, 0) for m in from_dates],
                "borderColor": "#3b82f6",
                "backgroundColor": "rgba(59, 130, 246, 0.1)",
                "fill": True,
            },
            {
                "label": _("Hires"),
                "data": [hires_map.get(m, 0) for m in from_dates],
                "borderColor": "#10b981",
                "backgroundColor": "rgba(16, 185, 129, 0.1)",
                "fill": True,
            },
        ],
    }


def get_revenue_chart_data(request):
    """Revenue breakdown — last 6 months."""
    months_labels = []
    from_dates = []
    for i in range(5, -1, -1):
        d = timezone.now() - timedelta(days=i * 30)
        months_labels.append(d.strftime("%b %Y"))
        from_dates.append(d.strftime("%Y-%m"))

    from_date = timezone.now() - timedelta(days=180)

    invoices_by_month = (
        Invoice.objects
        .filter(status='paid', paid_at__gte=from_date)
        .annotate(month=TruncMonth('paid_at'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )
    payroll_by_month = (
        PayrollRecord.objects
        .filter(status='paid', created_at__gte=from_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('gross_amount'))
        .order_by('month')
    )

    inv_map = {str(r['month'])[:7]: float(r['total']) for r in invoices_by_month}
    pay_map = {str(r['month'])[:7]: float(r['total']) for r in payroll_by_month}

    return {
        "labels": months_labels,
        "datasets": [
            {
                "label": _("Invoice Revenue (NPR)"),
                "data": [inv_map.get(m, 0) for m in from_dates],
                "backgroundColor": "#6366f1",
            },
            {
                "label": _("Payroll Revenue (NPR)"),
                "data": [pay_map.get(m, 0) for m in from_dates],
                "backgroundColor": "#f59e0b",
            },
        ],
    }


def get_social_engagement_data(request):
    """Engagement breakdown across social features."""
    return {
        "labels": [_("Posts"), _("Comments"), _("Likes"), _("Connections"), _("Follows"), _("Messages")],
        "datasets": [{
            "label": _("Platform Activity"),
            "data": [
                Post.objects.count(),
                Comment.objects.count(),
                Like.objects.count(),
                Connection.objects.filter(status='accepted').count(),
                Follow.objects.count(),
                Message.objects.count(),
            ],
            "backgroundColor": [
                "#3b82f6", "#10b981", "#f59e0b",
                "#6366f1", "#ec4899", "#8b5cf6"
            ],
        }]
    }

def get_top_posts(request):
    """Top 5 posts by likes."""
    top_posts = (
        Post.objects
        .annotate(likes_count=Count('likes'))
        .order_by('-likes_count')[:5]
    )
    return [
        {
            "id": post.id,
            "author": post.author.email,
            "content": post.content[:100] + ("..." if len(post.content) > 100 else ""),
            "likes": post.likes_count,
            "created_at": post.created_at.strftime("%Y-%m-%d"),
        }
        for post in top_posts
    ]

def get_top_stories(request):
    """Top 5 stories by likes."""
    top_stories = (
        Stori.objects
        .annotate(likes_count=Count('likes'))
        .order_by('-likes_count')[:5]
    )
    return [
        {
            "id": story.id,
            "author": story.author.email,
            "caption": story.caption[:100] + ("..." if len(story.caption) > 100 else ""),
            "likes": story.likes_count,
            "views": story.views_count,
            "created_at": story.created_at.strftime("%Y-%m-%d"),
        }
        for story in top_stories
    ]

def get_talent_insights(request):
    """Top skills by endorsement count — radar chart."""
    top_skills = (
        Skill.objects
        .annotate(user_count=Count('user_skills'))
        .order_by('-user_count')[:6]
    )
    return {
        "labels": [skill.name for skill in top_skills],
        "datasets": [{
            "label": _("Users with Skill"),
            "data": [skill.user_count for skill in top_skills],
            "backgroundColor": "rgba(236, 72, 153, 0.4)",
            "borderColor": "#ec4899",
        }]
    }


from django.core.serializers.json import DjangoJSONEncoder
import json

def dashboard_callback(request, context):
    """
    Callback to inject all dashboard data into context.
    Provides a more reliable way to render widgets by directly updating the context.
    """
    context.update({
        "kpi_stats": get_kpi_stats(request),
        "hiring_chart": json.dumps(get_hiring_chart_data(request), cls=DjangoJSONEncoder),
        "revenue_chart": json.dumps(get_revenue_chart_data(request), cls=DjangoJSONEncoder),
        "engagement_chart": json.dumps(get_social_engagement_data(request), cls=DjangoJSONEncoder),
        "talent_chart": json.dumps(get_talent_insights(request), cls=DjangoJSONEncoder),
    })
    return context
