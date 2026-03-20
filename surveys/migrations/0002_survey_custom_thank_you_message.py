from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='custom_thank_you_message',
            field=models.TextField(blank=True, help_text='متن شخصی\u200cسازی شده\u200cای که می\u200cخواهید بعد از پاسخ به نظرسنجی نمایش داده شود.', null=True, verbose_name='پیام تشکر شخصی\u200cسازی شده'),
        ),
    ]
