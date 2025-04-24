from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
def default_expiry(): # function for card expiry date
    return timezone.now() + timedelta(days=90)
    
class TbResults(models.Model):
    student_id = models.AutoField(primary_key=True, unique=True)
    student_name = models.TextField(blank=True, null=True, max_length=30)
    Maths = models.IntegerField(blank=True, null=True)
    English = models.IntegerField(blank=True, null=True)
    Economics = models.IntegerField(blank=True, null=True)
    Biology = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'TbResults'
        verbose_name_plural = 'Student Results'

    @property
    def Total(self):
        return sum(filter(None, [
            self.Maths,
            self.English,
            self.Economics,
            self.Biology
        ])) or 0

    @property
    def Avscore(self):
        subjects = [self.Maths, self.English, self.Economics, self.Biology]
        valid_scores = [s for s in subjects if s is not None]
        return self.Total / len(valid_scores) if valid_scores else 0

    @property
    def Grade(self):
        if self.Avscore >= 75: return 'A1'
        if self.Avscore >= 70: return 'B2'
        if self.Avscore >= 65: return 'B3'
        if self.Avscore >= 60: return 'C4'
        if self.Avscore >= 55: return 'C5'
        if self.Avscore >= 50: return 'C6'
        if self.Avscore >= 45: return 'D7'
        if self.Avscore >= 40: return 'E8'
        return 'F9'

    def __str__(self):
        return f"{self.student_name} ({self.student_id}) - {self.Grade}"

    def save(self, *args, **kwargs):
        # Ensure computed properties are accessible immediately after save
        super().save(*args, **kwargs)    


class TbCard(models.Model):
    serial = models.IntegerField(primary_key=True, unique=True)
    pin = models.CharField(unique=True, max_length=256) # Hashed PIN
    student_id = models.IntegerField( 
        null=True, blank=True)
    print_date = models.DateTimeField(auto_now_add=True)
    # django can not serialize lambda funcs
    # expiry = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=90))
    # so I create a regular function to do the same
    expiry = models.DateTimeField(default=default_expiry)
    usage_count = models.IntegerField(default=0) # Number of times the card has been used
    is_valid = models.BooleanField(default=True)

    def hash_pin(self, rawpin):
        '''Hashes the raw pin before saving in db'''
        self.pin = make_password(rawpin)
        self.save()
    
    def check_pin(self, rawpin):
        '''verify the raw pin with the hashed one'''
        return check_password(self.pin, rawpin)
    
    class Meta:
        db_table = 'TbCard'  # This ensures the table name matches your original

    def __str__(self):
        return f"Card {self.serial} (PIN: {self.pin})"
    
    
    
    
class TbTransact(models.Model):
    id = (models.AutoField(primary_key=True, unique=True))
    student_id = models.ForeignKey(TbResults, on_delete=models.CASCADE)
    serial = models.ForeignKey(TbCard, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    card_use_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'TbTransact'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"Transaction {self.id} - {self.student_id}"
    
class TbUsed(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    student_id = models.ForeignKey(TbResults, on_delete=models.CASCADE)
    serial = models.ForeignKey(TbCard, on_delete=models.CASCADE)
    last_date = models.DateTimeField (auto_now_add=True)
    
    class Meta:
        db_table = "TbUsed"
        verbose_name_plural = 'Used Cards'
        
    def __str__(self):
        return f"Used Card {self.serial} - {self.student_id}"