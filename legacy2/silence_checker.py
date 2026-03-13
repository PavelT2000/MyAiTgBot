from datetime import datetime, timedelta
from scheduler import scheduler,send_silence_signal_to_ai


async def reset_silence_timer(user_id:int):
    """Рестартить таймер тишины в диалоге для конкретного пользователя"""
    job_id = f"silence_{user_id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        print(f"⏱ Таймер тишины для {user_id} сброшен.")

    # 2. Ставим новую задачу на +10 минут от текущего момента
    run_at = datetime.now() + timedelta(minutes=10)
    scheduler.add_job(
        send_silence_signal_to_ai,
        'date',
        run_date=run_at,
        args=[user_id],
        id=job_id,
        replace_existing=True
    )
    print(f"⏱ Новый таймер тишины установлен на {run_at.strftime('%H:%M:%S')}")