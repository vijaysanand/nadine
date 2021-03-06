# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Moving the data that once was in the settings file into the data model"

        "Create the new plans to match our existing plans"
        basicPlan = orm.MembershipPlan(name="Basic",monthly_rate="50",dropin_allowance="3",daily_rate="20",deposit_amount="0",has_desk=False)
        basicPlan.description = "The most basic membership plan."
        basicPlan.save()
        pt5Plan = orm.MembershipPlan(name="PT5",monthly_rate="75",dropin_allowance="5",daily_rate="20",deposit_amount="0",has_desk=False)
        pt5Plan.description = "Part-Time 5 membership"
        pt5Plan.save()
        pt10Plan = orm.MembershipPlan(name="PT10",monthly_rate="150",dropin_allowance="10",daily_rate="20",deposit_amount="0",has_desk=False)
        pt10Plan.description = "Part-Time 10 membership"
        pt10Plan.save()
        pt15Plan = orm.MembershipPlan(name="PT15",monthly_rate="225",dropin_allowance="15",daily_rate="20",deposit_amount="0",has_desk=False)
        pt15Plan.description = "Part-Time 15 membership"
        pt15Plan.save()
        residentPlan = orm.MembershipPlan(name="Resident",monthly_rate="475",dropin_allowance="5",daily_rate="20",deposit_amount="500",has_desk=True)
        residentPlan.description = "Resident members have a desk and 24/7 access to the space"
        residentPlan.save()
        otherPlan = orm.MembershipPlan(name="Other",monthly_rate="0",dropin_allowance="0",daily_rate="20",deposit_amount="0",has_desk=False)
        otherPlan.save()

        "Update all the existing memberships to link to our new plans"
        for membership in orm.Membership.objects.all():
            if membership.plan == 'Basic':
                membership.membership_plan = basicPlan
            elif membership.plan == 'PT5':
                membership.membership_plan = pt5Plan
            elif membership.plan == 'PT10':
                membership.membership_plan = pt10Plan
            elif membership.plan == 'PT15':
                membership.membership_plan = pt15Plan
            elif membership.plan == 'Resident':
                membership.membership_plan = residentPlan
                if not membership.end_date:
                   membership.deposit_amount = residentPlan.deposit_amount
            elif membership.plan == 'Regular':
                "Special case that needs to be pulled out and handled seperately"
                membership.membership_plan = otherPlan
                membership.daily_rate = membership.membership_plan.daily_rate
                membership.dropin_allowance = 30
                membership.save()
                continue
            else:
                membership.membership_plan = otherPlan
            membership.daily_rate = membership.membership_plan.daily_rate
            membership.dropin_allowance = membership.membership_plan.dropin_allowance
            membership.has_desk = membership.membership_plan.has_desk
            membership.save()


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'staff.bill': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Bill'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'dropins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bills'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['staff.DailyLog']"}),
            'guest_dropins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'guest_bills'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['staff.DailyLog']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bills'", 'to': "orm['staff.Member']"}),
            'membership': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Membership']", 'null': 'True', 'blank': 'True'}),
            'new_member_deposit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paid_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'guest_bills'", 'null': 'True', 'to': "orm['staff.Member']"})
        },
        'staff.billinglog': {
            'Meta': {'ordering': "['-started']", 'object_name': 'BillingLog'},
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'staff.dailylog': {
            'Meta': {'ordering': "['-visit_date', '-created']", 'object_name': 'DailyLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 8, 1, 15, 24, 33, 501977)', 'auto_now_add': 'True', 'blank': 'True'}),
            'guest_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'guest_of'", 'null': 'True', 'to': "orm['staff.Member']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'daily_logs'", 'to': "orm['staff.Member']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': "'True'"}),
            'payment': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'visit_date': ('django.db.models.fields.DateField', [], {})
        },
        'staff.exittask': {
            'Meta': {'ordering': "['order']", 'object_name': 'ExitTask'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'staff.exittaskcompleted': {
            'Meta': {'object_name': 'ExitTaskCompleted'},
            'completed_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Member']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.ExitTask']"})
        },
        'staff.howheard': {
            'Meta': {'ordering': "['name']", 'object_name': 'HowHeard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'staff.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'staff.member': {
            'Meta': {'ordering': "['user__first_name', 'user__last_name']", 'object_name': 'Member'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'email2': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'has_kids': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'howHeard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.HowHeard']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Industry']", 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Neighborhood']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'phone2': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'promised_followup': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'self_employed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'staff.membership': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'Membership'},
            'daily_rate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deposit_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dropin_allowance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'guest_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'monthly_guests'", 'null': 'True', 'to': "orm['staff.Member']"}),
            'has_desk': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': "orm['staff.Member']"}),
            'membership_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.MembershipPlan']", 'null': 'True'}),
            'monthly_rate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'staff.membershipplan': {
            'Meta': {'object_name': 'MembershipPlan'},
            'daily_rate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deposit_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'dropin_allowance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'has_desk': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_rate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'staff.neighborhood': {
            'Meta': {'ordering': "['name']", 'object_name': 'Neighborhood'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'staff.onboard_task': {
            'Meta': {'ordering': "['order']", 'object_name': 'Onboard_Task'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'staff.onboard_task_completed': {
            'Meta': {'unique_together': "(('member', 'task'),)", 'object_name': 'Onboard_Task_Completed'},
            'completed_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Member']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Onboard_Task']"})
        },
        'staff.transaction': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Transaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'bills': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'transactions'", 'symmetrical': 'False', 'to': "orm['staff.Bill']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['staff.Member']"}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'open'", 'max_length': '10'})
        }
    }

    complete_apps = ['staff']
