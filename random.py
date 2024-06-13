from datetime import date

def days_to_date(target_date_str):
  target_date = date.fromisoformat(target_date_str)
  today = date.today()
  days_diff = target_date - today
  if days_diff:
    return days_diff.days
  return 0

