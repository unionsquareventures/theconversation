import app.basic
import tornado.web
import settings
import datetime
from lib import brittbotdb


###########################
### Creates the initial intro email
### /admin/brittbot
###########################
class Index(app.basic.BaseHandler):
	@tornado.web.authenticated
	def get(self):
		sent = self.get_argument('sent', '')
		err = self.get_argument('err', '')

		# Form fields
		to_name = self.get_argument('to_name', '')
		to_email = self.get_argument('to_email', '')
		for_name = self.get_argument('for_name', '')
		for_email = self.get_argument('for_email', '')
		purpose = self.get_argument('purpose', '')
		form = {'to_name': to_name, 'to_email': to_email, 'for_name': for_name, 'for_email': for_email, 'purpose': purpose}

  		self.render('admin/brittbot/index.html', form=form, err=err, sent=sent)

	# If form is submitted correctly, send initial email
	@tornado.web.authenticated
	def post(self):
		# Get submitted form data
		to_name = self.get_argument('to_name', '')
		to_email = self.get_argument('to_email', '')
		for_name = self.get_argument('for_name', '')
		for_email = self.get_argument('for_email', '')
		purpose = self.get_argument('purpose', '')
		intro = {'to_name': to_name, 'to_email': to_email, 'for_name': for_name, 'for_email': for_email, 'purpose': purpose}

		# TODO: Server side error handling? 

		# Save intro to database
		try:
			intro['sent_initial'] = datetime.date.today()
			brittbotdb.save_intro(intro)
		except:
			pass # multiple redirects in function apparently a problem
			#self.redirect('brittbot?err=%s' % 'Failed to save file to database. Email was not sent.')

		# Send initial email
		try:
			subject = "Intro to %s?" % intro['for_name']
			response_url = settings.get('BB_RESPONSE_URL')
			#text_body = 'Hi %s, %s wants to meet with you to %s If you are open to the connection please email reply to brittany@usv.com. This will automatically generate an email from brittany@usv.com to connect the two of you. Thanks! Brittany' % (intro['to_name'], intro['for_name'], intro['purpose'])
			body = 'Hi %s,<br> %s wants to meet with you to %s <br><br>If you are open to the connection please <a href="%s?id=%s">click here</a>. This will automatically generate an email from brittany@usv.com to connect the two of you. <br><br> Thanks! Brittany' % (intro['to_name'], intro['for_name'], intro['purpose'], response_url, intro['id'])
			self.send_email(settings.get('BB_EMAIL_HOST_USER'), intro['to_email'], subject, html_body)
			self.redirect('brittbot?sent=%s (%s)' % (intro['to_name'], intro['to_email'])) # Always redirect after successful POST
		except:
			brittbotdb.remove_intro(intro)
			self.redirect('brittbot?err=%s' % 'Email failed to send.')


###########################
### Creates the actual intro email
### once the initial user has acquiesced
### /admin/brittbot/response
###########################
class Response(app.basic.BaseHandler):		
	def get(self):
		# Get intro from database
		intro_id = self.get_argument('id', '')
		try:
			intro = brittbotdb.get_by_id(intro_id)
		except:
			self.render('admin/brittbot/response.html', err="Sorry! I couldn't find this intro in my database. Please contact brittany@usv.com")

		if 'connected' in intro.keys():
			self.render('admin/brittbot/response.html', err="Your email has already been sent! Stop clicking the link!")

		subject = "%s <-> %s" % (intro.for_name, intro.to_name)
		email_body = 'Great that you guys are connecting!'
		#send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [intro.to_email, intro.for_email], fail_silently=False)
		try:
			self.send_email(settings.get('BB_EMAIL_HOST_USER'), [intro['to_email'], intro.for_email], subject, body)
		except: 
			self.render('admin/brittbot/response.html', err="Sorry, there was a problem with our email server. Please try again or contact brittany@usv.com")
		
		intro['connected'] = datetime.date.today()
		brittbotdb.save_intro(intro)
		return self.render('admin/brittbot/response.html', intro=intro)

'''
Handles response from the initial email.
Currently, the link emailed out modifies the database with a GET request, which is not ideal.
But there is no way to let most email client include a POST link (and for good reason). 
'''
'''def response(request, intro_id):
	try:
		intro = Intro.objects.get(id=intro_id)
	except:
		return render_to_response('response.html', {'error': "Sorry! I couldn't find this intro in my database. Please contact brittany@usv.com"}, context_instance=RequestContext(request))

	if intro.connected is not None:
		return render_to_response('response.html', {'error': "Your email has already been sent! Stop clicking the link!", 'intro': intro}, context_instance=RequestContext(request))

	email_subject = "%s <-> %s" % (intro.for_name, intro.to_name)
	email_body = 'Great that you guys are connecting!'
	send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [intro.to_email, intro.for_email], fail_silently=False)
	intro.connected = datetime.date.today()
	intro.save()
	return render_to_response('response.html', {'intro': intro}, context_instance=RequestContext(request))
'''

''' From http://rosettacode.org/wiki/Send_an_email#Python '''
'''
import smtplib
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
  
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
'''
''' Old email crap
#msg = EmailMultiAlternatives(email_subject, text_body, settings.get('EMAIL_HOST_USER'), [to_email])
#msg.attach_alternative(html_body, "text/html")
#msg.send()	

self.sendemail(from_addr    = settings.get('BB_EMAIL_HOST_USER'), 
          to_addr_list = intro['to_email'],
          cc_addr_list = settings.get('BB_EMAIL_HOST_USER'), 
          subject      = subject, 
          message      = html_body, 
          login        = settings.get('BB_EMAIL_HOST_USER'),
          password     = settings.get('BB_EMAIL_HOST_PASSWORD'))
'''


