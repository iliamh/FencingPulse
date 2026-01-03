"""تولید توضیح فارسی و تمرین‌های پیشنهادی بر اساس امتیاز حرکتی."""

from typing import Dict, List

def generate_report(summary: Dict[str, float], similarity: Dict[str, float]) -> Dict[str, any]:
    """ایجاد متن توضیحی و تمرین‌های اصلاحی برای کاربر.

    summary: خروجی summarize_pose_results
    similarity: خروجی compare_to_prototypes
    بر اساس امتیاز و شباهت‌ها، توصیه‌هایی تولید می‌شود.
    """
    score = summary.get("pose_score", 0.0)
    desc = ""
    recommendations: List[str] = []
    if score >= 75:
        desc = "عملکرد حرکتی شما عالی است و بسیار به الگوهای ایده‌آل نزدیک هستید."
    elif score >= 50:
        desc = "عملکرد حرکتی شما متوسط است. چند نقطه برای بهبود وجود دارد."
    else:
        desc = "عملکرد حرکتی شما نیازمند توجه و تمرین است."

    # تمرین‌های پیشنهادی ساده
    if summary.get("knee_angle_mean", 0) > 100:
        recommendations.append("تمرین تقویت عضلات چهارسر ران برای بهبود کنترل زاویه زانو")
    if summary.get("hip_angle_mean", 0) < 80:
        recommendations.append("تمرین کششی برای افزایش انعطاف لگن")
    if summary.get("cadence_mean", 0) < 1.5:
        recommendations.append("تمرین سرعت قدم‌رو برای افزایش cadence")
    # اگر هنوز کمتر از 3 تمرین داریم، پیشنهاد عمومی بدهیم
    while len(recommendations) < 3:
        recommendations.append("تمرین تعادل و ثبات مرکزی بدن")

    # تفاوت با پروتوتایپ‌ها
    sim1 = similarity.get("proto1_similarity", 0.0)
    sim2 = similarity.get("proto2_similarity", 0.0)
    diff_report = "شما به الگو ۱ {:.0%} و به الگو ۲ {:.0%} شباهت دارید.".format(sim1, sim2)

    return {
        "score": score,
        "description": desc,
        "recommendations": recommendations,
        "similarity": similarity,
        "difference_report": diff_report
    }