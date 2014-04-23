from datetime import datetime
import settings

class datetime(datetime):
	def today(self):
		if settings.get('ENVIRONMENT') == "dev":
			return datetime.date('2014-02-01')
		else:
			return datetime.today()