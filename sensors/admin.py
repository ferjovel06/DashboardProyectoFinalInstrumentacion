from django.contrib import admin

from .models import Measure, Suggestion

@admin.register(Measure)
class MeasuresAdmin(admin.ModelAdmin):
    list_display = ('temperature', 'ph', 'tds', 'ec', 'timestamp')
    list_filter = ('temperature', 'ph', 'tds', 'ec')
    search_fields = ('temperature', 'ph', 'tds', 'ec')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 20
    actions = ['export_as_csv']
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="measurements.csv"'

        writer = csv.writer(response)
        writer.writerow(['Temperature', 'pH', 'TDS', 'Timestamp'])

        for measurement in queryset:
            writer.writerow([measurement.temperature, measurement.ph, measurement.tds, measurement.timestamp])

        return response
    export_as_csv.short_description = "Export selected measurements as CSV"

@admin.register(Suggestion)
class SuggestionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'description', 'timestamp')
    list_filter = ('title', 'subtitle')
    search_fields = ('title', 'subtitle', 'description')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 20