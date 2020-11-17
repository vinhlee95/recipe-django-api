from django.contrib import admin
from django.contrib.auth import admin as authAdmin
from core import models
# Translation
from django.utils.translation import gettext as _

class UserAdmin(authAdmin.UserAdmin):
	ordering = ['id']
	list_display = ['name', 'email']
	fieldsets = (
		# (Section name, {fields: })
		(None, {
			'fields': ('email', 'password')
		}),
		(_('Personal info'), {
			'fields': ('name',)
		}),
		(_('Permissions'), {
			'fields': ('is_active', 'is_staff', 'is_superuser')
		}),
		(_('Important dates'), {
			'fields': ('last_login',)
		})
	)
	add_fieldsets = (
		(None, {
			'fields': ('email', 'password')
		}),
	)

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)