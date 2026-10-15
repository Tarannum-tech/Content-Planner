# from datetime import datetime, timedelta

# def content_calendar(ideas: list, start_date=None, posts_per_week=3):
#     if not start_date:
#         start_date = datetime.now()

#     gap_days = max(1, 7 // posts_per_week)
#     calendar = []

#     for i, idea in enumerate(ideas):
#         day = start_date + timedelta(days=i * gap_days)
#         calendar.append({
#             "date": day.strftime("%Y-%m-%d"),
#             "day": day.strftime("%A"),
#             "idea": idea
#         })
#     return calendar

from datetime import datetime, timedelta

def generate_calendar(ideas: list, start_date=None, posts_per_week=3):
    if not start_date:
        start_date = datetime.now()

    gap_days = max(1, 7 // posts_per_week)
    calendar = []

    for i, idea in enumerate(ideas):
        day = start_date + timedelta(days=i * gap_days)
        calendar.append({
            "date": day.strftime("%Y-%m-%d"),
            "day": day.strftime("%A"),
            "idea": idea
        })
    return calendar



