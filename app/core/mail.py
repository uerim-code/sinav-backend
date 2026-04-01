"""E-posta gonderim servisi — Resend API."""

import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_mail(to_email: str, subject: str, body_html: str) -> bool:
    """Resend API ile e-posta gonder."""
    if not settings.RESEND_API_KEY:
        logger.info(f"RESEND_API_KEY yok — {to_email} adresine gonderilmedi: {subject}")
        return False

    try:
        import resend
        resend.api_key = settings.RESEND_API_KEY

        # html'den plain text versiyonu olustur
        import re as _re
        plain = _re.sub(r'<[^>]+>', '', body_html)
        plain = _re.sub(r'\s+', ' ', plain).strip()

        result = resend.Emails.send({
            "from": f"Sinav Otomasyon <{settings.MAIL_FROM}>",
            "to": [to_email],
            "reply_to": "destek@unvportal.com",
            "subject": subject,
            "html": body_html,
            "text": plain,
            "headers": {
                "List-Unsubscribe": f"<mailto:{settings.MAIL_FROM}?subject=unsubscribe>",
            },
        })
        rid = getattr(result, "id", None) or (result.get("id") if isinstance(result, dict) else str(result))
        logger.info(f"Mail gonderildi (Resend): {to_email} — {subject} — id={rid}")
        return True
    except Exception as e:
        logger.error(f"Mail gonderilemedi: {to_email} — {e}")
        return False


def bildirim_maili(to_email: str, baslik: str, mesaj: str, link: str = None):
    """Bildirim e-postasi gonder."""
    link_html = f"""
    <tr><td style="padding:16px 0 0;">
      <a href="{link}" style="display:inline-block;background-color:#6366f1;color:#ffffff;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;font-size:14px;">Goruntule</a>
    </td></tr>""" if link else ''

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="font-family:Arial,sans-serif;background-color:#f5f5f5;margin:0;padding:0;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f5;">
    <tr><td align="center" style="padding:32px 16px;">
      <table role="presentation" width="520" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:8px;">
        <tr>
          <td style="background-color:#4f46e5;padding:20px 24px;border-radius:8px 8px 0 0;">
            <h2 style="margin:0;color:#ffffff;font-size:16px;">Sinav Otomasyon</h2>
          </td>
        </tr>
        <tr>
          <td style="padding:24px;color:#1f2937;font-size:14px;line-height:1.6;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
              <tr><td><h3 style="margin:0 0 8px;font-size:15px;color:#1f2937;">{baslik}</h3></td></tr>
              <tr><td style="color:#6b7280;font-size:13px;line-height:1.6;">{mesaj}</td></tr>
              {link_html}
            </table>
          </td>
        </tr>
        <tr>
          <td style="background-color:#f5f5f5;padding:14px 24px;text-align:center;font-size:11px;color:#9ca3af;border-radius:0 0 8px 8px;">
            Bu e-posta Sinav Otomasyon sistemi tarafindan gonderilmistir.
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""
    return send_mail(to_email, f"Sinav Otomasyon — {baslik}", html)
