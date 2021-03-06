from django.db import models

FREQUENCY = (
    ('dly', 'Daily'),
    ('wly', 'Weekly'),
    ('mly', 'Monthly'),
    ('off', 'Off'),
)


class Alert(models.Model):
    alertName = models.CharField(
        verbose_name='a name for the alert',
        max_length=75
    )
    alertText = models.CharField(
        verbose_name='the text of an alert created by a user',
        max_length=2500
    )
    alertFrequency = models.CharField(
        verbose_name='the rate chosen by the user for the alert',
        choices=FREQUENCY,
        max_length=10
    )
    sendNegativeAlert = models.BooleanField(
        verbose_name='should alerts be sent when there are no hits during a '
                     'specified period',
        default=False
    )
    lastHitDate = models.DateTimeField(
        verbose_name='the exact date and time stamp that the alert last sent '
                     'an email',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return 'Alert ' + str(self.pk) + ': ' + self.alertName

    class Meta:
        verbose_name = 'alert'
        ordering = ['alertFrequency', 'alertText']
        db_table = 'Alert'
