"""
Copyright 2014-2016 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os

from os.path import join 

from django.db import models
from urlparse import urlparse
from django.core.urlresolvers import reverse
from pytz import timezone
from django.contrib.sites.models import Site

from django.contrib.auth.models import User

from rulesets.models            import Ruleset

from fae2.settings import APP_DIR

# Create your models here.

RESULT_VALUE = {
  'UNDEFINED'      : 0,
  'NOT_APPLICABLE' : 1,
  'PASS'           : 2,
  'MANUAL_CHECK'   : 3,
  'WARNING'        : 4,
  'VIOLATION'      : 5
}  

IMPLEMENTATION_STATUS_CHOICES = (
    ('U',   'Undefined'),
    ('NA',  'Not applicable'),
    ('NI',  'Not Implemented'),
    ('PI',  'Partial Implementation'),
    ('AC',  'Almost Complete'),
    ('C',   'Complete'),
)


MC_STATUS_CHOICES = (
    ('NC',  'Not Checked'),
    ('NA',  'Not Applicable'),
    ('P',   'Passed'),
    ('F',   'Fail'),
)

# ---------------------------------------------------------------
#
# Pages Summary Object
#
# ---------------------------------------------------------------

class PagesSummary:

  def __init__(self):

    self.pages_violation = 0
    self.pages_warning = 0
    self.pages_manual_check = 0
    self.pages_passed = 0
    self.pages_not_applicable = 0

  def update_summary(self, result):

    if result == RESULT_VALUE['VIOLATION']:
      self.pages_violation += 1
    elif result == RESULT_VALUE['WARNING']:  
      self.pages_warning += 1
    elif result == RESULT_VALUE['MANUAL_CHECK']:  
      self.pages_manual_check += 1
    elif result == RESULT_VALUE['PASS']:  
      self.pages_passed += 1
    elif result == RESULT_VALUE['NOT_APPLICABLE']:  
      self.pages_not_applicable += 1  


# ---------------------------------------------------------------
#
# RuleResult
#
# ---------------------------------------------------------------

class RuleResult(models.Model):
  result_value           = models.IntegerField(default=0)

  implementation_pass_fail_score  = models.IntegerField(default=-1)
  implementation_score            = models.IntegerField(default=-1)

  implementation_pass_fail_status  = models.CharField("Implementation Pass/Fail Status",  max_length=2, choices=IMPLEMENTATION_STATUS_CHOICES, default='U')
  implementation_status            = models.CharField("Implementation Status",  max_length=2, choices=IMPLEMENTATION_STATUS_CHOICES, default='U')

  manual_check_status    = models.CharField("Manual Check Status",  max_length=2, choices=MC_STATUS_CHOICES, default='NC')

  class Meta:
        abstract = True


# ---------------------------------------------------------------
#
# RuleGroupResult
#
# ---------------------------------------------------------------

class RuleGroupResult(RuleResult):
  rules_violation    = models.IntegerField(default=0)
  rules_warning      = models.IntegerField(default=0)
  rules_manual_check = models.IntegerField(default=0)
  rules_passed       = models.IntegerField(default=0)
  rules_na           = models.IntegerField(default=0)

  rules_with_hidden_content = models.IntegerField(default=0)

  class Meta:
        abstract = True


# Create your models here.


EVAL_STATUS = (
    ('-', 'Created'),
    ('I', 'Initalized'),
    ('A', 'Analyzing'),
    ('S', 'Saving'),
    ('C', 'Complete'),
    ('E', 'Error'),
    ('SUM', 'Summary'),
)

FOLLOW_CHOICES = (
  (1, 'Specified domain only'),
  (2, 'Next-level subdomains')
)


DEPTH_CHOICES = (
  (1, 'Top-level page only'),
  (2, 'Include second-level pages'),
  (3, 'Include third-level pages')
)
      
WAIT_TIME_CHOICES = (
  (30000,  ' 30 seconds'),
  (45000,  ' 45 seconds'),
  (60000,  ' 60 seconds'),
  (90000,  ' 90 seconds'),
  (120000, '120 seconds')
)   

MAX_PAGES_CHOICES = (
  (0,   ' All pages'),
  (5,   '   5 pages'),
  (10,  '  10 pages'),
  (25,  '  25 pages')
)  

LAST_REPORT_TYPE_CHOICES = (
  ('rules',   'Summary'),
  ('pages',   'All Pages'),
  ('page',    'Page')
)  

LAST_VIEW_CHOICES = (
  ('rc',   'Rule Category'),
  ('gl',   'WCAG Guideline'),
  ('rs',   'Rule Scope')
)  

# ---------------------------------------------------------------
#
# WebsiteReport
#
# ---------------------------------------------------------------

class WebsiteReport(RuleGroupResult):

  id    = models.AutoField(primary_key=True)

  user  = models.ForeignKey(User, editable=True, related_name="reports")
    
  slug  = models.SlugField(max_length=256, default="", blank=True, editable=False, unique=True)

  title    = models.CharField("Title",  max_length=1024, default="", blank=False)
  
  url        = models.URLField("URL",      max_length=1024, default="", blank=False)
  follow     = models.IntegerField("Follow Links in", choices=FOLLOW_CHOICES, default=1, blank=False)
  depth      = models.IntegerField("Depth of Evaluation", choices=DEPTH_CHOICES, default=2, blank=False)
  max_pages  = models.IntegerField("Maximum Pages", choices=MAX_PAGES_CHOICES, default=0, blank=False)
  ruleset    = models.ForeignKey(Ruleset, default=2, blank=False)

  browser_emulation    = models.CharField("Browser Emulation", max_length=32, default="FIREFOX")

  wait_time            = models.IntegerField("How long to wait for website to load resources (in milliseconds)", choices=WAIT_TIME_CHOICES, default=90000)
  
  span_sub_domains     = models.CharField("Span Sub-Domains (space separated)",    max_length=1024, default="", blank=True)
  exclude_sub_domains  = models.CharField("Exclude Sub-Domains (space separated)", max_length=1024, default="", blank=True)
  include_domains      = models.CharField("Include Domains (space separated)",     max_length=1024, default="", blank=True)
  authorization        = models.TextField("Authentication Information",            max_length=8192, default="", blank=True)

  page_count = models.IntegerField("Number of Pages",  default=0)  

  # Archiving information

  archive  = models.BooleanField(default=False)
  delete   = models.BooleanField(default=False)
  stats    = models.BooleanField(default=False)

  # Report History Information
  
  last_viewed        = models.DateTimeField(auto_now=True, editable=False)
  last_report_type   = models.CharField('Last Report Type', max_length=16, default="rules", choices=LAST_REPORT_TYPE_CHOICES)
  last_view          = models.CharField('Last Viewed', max_length=4, default="rc", choices=LAST_VIEW_CHOICES)
  last_group         = models.CharField('Last Group', max_length=32, default="")
  last_page          = models.IntegerField('Last Page Viewed', default=1)
  
  # fae-util and fae20 processing information

  created      = models.DateTimeField(auto_now_add=True, editable=False)
  status       = models.CharField('Status',  max_length=10, choices=EVAL_STATUS, default='-')  
  
  # processining information    
  processing_time        = models.IntegerField(default=-1)
  processed_urls_count   = models.IntegerField(default=-1)
  unprocessed_urls_count = models.IntegerField(default=-1)
  filtered_urls_count    = models.IntegerField(default=-1)

  data_dir_slug            = models.SlugField(max_length=50, editable=False)
  data_directory           = models.CharField('Data Directory',           max_length=1024, default="")
  data_property_file       = models.CharField('Property File Name',       max_length=1024, default="")
  data_authorization_file  = models.CharField('Authorization File Name',  max_length=1024, default="", blank=True)
  data_multiple_urls_file  = models.CharField('Multiple URLs File Name',  max_length=1024, default="", blank=True)

  log_file                 = models.CharField('Log file',       max_length=1024, default="")
  
  # Rule results summary information
    
  class Meta:
    verbose_name        = "Report"
    verbose_name_plural = "Reports"
    ordering = ['-created']

  def __str__(self):
    return "Website Report: " + self.title

  def save(self):

    if len(self.data_dir_slug) == 0:
      DIR = APP_DIR

      count = len(WebsiteReport.objects.filter(user=self.user)) + 1

      self.data_dir_slug = "report_" + "%05d" % (count,)

      self.data_directory          = DIR + "data/" + self.user.username + "/" + self.data_dir_slug 
      self.data_property_file      = self.data_directory + "/" +  self.data_dir_slug + ".properties"
      
      if len(self.authorization) > 0:
        self.data_authorization_file = self.data_directory + "/" +  self.data_dir_slug + ".authorization"
      else:  
        self.data_authorization_file = ""

      self.log_file = self.data_directory + "/" +  self.data_dir_slug + ".log" 
    
      self.status = '-' 

    super(WebsiteReport, self).save() # Call the "real" save() method        

  def delete_data_files(self):
    path = self.data_directory
    try:
      for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*.json'):
          os.remove(join(path,file))
    except:
      return False   

    return True    

  def set_status_initialized(self):
    self.status = 'I'
    self.save()

  def set_status_analyzing(self):
    self.status = 'A'
    self.save()

  def set_status_saving(self):
    self.status = 'S'
    self.save()

  def set_status_complete(self):
    self.delete_data_files()
    self.status = 'C'
    self.save()

  def set_status_error(self):
    self.delete_data_files()
    self.status = 'E'
    self.save()

  def set_status_summary(self):
    self.status = 'S'
    self.save()

  def get_first_page(self):
    return self.page_all_results.all()[0]

  def set_rule_numbers(self):
    ws_result = self.ws_all_results.last()
    num = 1
    for wsrr in ws_result.ws_rule_results.all():
      wsrr.rule_number = num
      wsrr.save()
      num += 1  

  def set_page_numbers(self):
    num = 1
    for pr in self.page_all_results.all():
      pr.page_number = num
      pr.save()
      num += 1     

  def get_pages_summary(self, view=False, group=False):
      ps = PagesSummary()

      for pr in self.page_all_results.all():
        if view == 'rs':
          pr = pr.page_rs_results.get(rule_category__slug=group)
        elif view == 'gl':
          pr = pr.page_gl_results.get(guideline__slug=group)
        elif view == 'rc':
          pr = pr.page_rc_results.get(rule_category__slug=group)

        ps.update_summary(pr.result_value) 

      return ps


  def get_page_count(self):
    if self.status == 'C' or self.status == 'E' or self.status == 'D':
        return self.page_count

    return self.get_processing_status().processed 

  def toJSON(self):
    tz = timezone(str(self.user.profile.timezone))

    json = {}
    json['id']          = 'r' + str(self.id)
    json['slug']        = self.slug
    json['title']       = self.title
    json['status']      = self.status
    json['archive']     = self.archive
    json['date']        = self.created.astimezone(tz)
    json['ruleset']     = self.ruleset.title
    json['ruleset_url'] = reverse('ruleset', args=[self.ruleset.slug])
    json['report_url']  = reverse('report_rules',  args=[self.slug, 'rc'])
    json['report_page_url']  = ""
    if self.page_count > 0:
      json['report_page_url']  = reverse('report_page',  args=[self.slug, 'rc', 1])
    json['depth']       = self.depth
    json['url']         = self.url
    json['page_count']  = self.get_page_count()

    return json


  def get_processing_status(self):
  
    class processing_info:
    
       def __init__(self):
         self.status = ''
         self.url    = ''
         self.processed  = -1
         self.unprocessed = 0
         self.filtered  = 0
         self.time  = 0.0
         self.login_attempts = 0 
         self.login_success  = 0
         self.login_fail     = 0  

    pi = processing_info()

    fname = self.data_directory + "/data/status.txt"
#    print('[WebsiteReport][get_processing_status] ' + APP_DIR)
#    print('[WebsiteReport][get_processing_status] ' + fname)

    try:
      file = open( fname, "r")
      for line in file.readlines():   
        if line.find("status=") >= 0:
          pi.status = line[7:]
        elif line.find("url=") >= 0:
          pi.url = line[4:]
        elif line.find("unprocessed=") >= 0:
          pi.unprocessed = int(line[12:])
        elif line.find("processed=") >= 0:
          pi.processed = int(line[10:])
        elif line.find("filtered=") >= 0:
          pi.filtered = int(line[9:])
        elif line.find("time=") >= 0:
          pi.time = float(line[5:])
        elif line.find("login_attempts=") >= 0:
          pi.login_attempts = int(line[15:])
        elif line.find("login_success=") >= 0:
          pi.login_success = int(line[14:])
        elif line.find("login_fail=") >= 0:
          pi.login_fail = int(line[11:])
        
    except:
      pi.status = "file not found"  
    
    return pi

  def broken_urls(self):
    urls = []

    for url in self.processed_urls.all():
      if url.http_status_code != 200:
        urls.append(url) 

    return urls    


# ---------------------------------------------------------------
#
# ProcessedURL
#
# ---------------------------------------------------------------
 
class ProcessedURL(models.Model):
  processed_url_id = models.AutoField(primary_key=True)

  ws_report  = models.ForeignKey(WebsiteReport, related_name="processed_urls")
  
  page_seq_num    = models.IntegerField(default=-1)

  url_requested    = models.URLField( 'Processed URL',  max_length=4096)
  url_returned     = models.URLField( 'Returned URL',   max_length=4096)
  redirect         = models.BooleanField("Server redirect", default=False)
  http_status_code = models.IntegerField('http status code')  
  
  url_referenced   = models.URLField( 'Referenced URL', max_length=4096)
 
  dom_time   = models.IntegerField('Loading DOM time')  
  link_time  = models.IntegerField('Retreive links tIme')   
  event_time = models.IntegerField('Event time')  
  eval_time  = models.IntegerField('Evaluation time')   
  save_time  = models.IntegerField('Saving results time')   
  total_time = models.IntegerField('Total processing time')

  class Meta:
    verbose_name        = "URL: Processed"
    verbose_name_plural = "URL: Processed"
    ordering = ['http_status_code', 'url_returned', 'total_time']

  def __unicode__(self):
    return self.url_returned + " (" + str(self.total_time) + " milliseconds)" 
    
  def get_url_requested(self):
    if len(self.url_requested) > 50:
      return self.url_requested[:50] + '...... '   
    else:
      return self.url_requested   
      

  def get_url_returned(self):
    if len(self.url_returned) > 50:
      return self.url_returned[:50] + '...... '   
    else:
      return self.url_returned  

  def get_reference_url(self):
    if len(self.url_referenced) > 50:
      return self.url_referenced[:50] + '...... '   
    else:
      return self.url_referenced  

# ---------------------------------------------------------------
#
# UnprocessedURL
#
# ---------------------------------------------------------------
 
class UnprocessedURL(models.Model):
  unprocessed_url_id = models.AutoField(primary_key=True)

  ws_report  = models.ForeignKey(WebsiteReport, related_name="unprocessed_urls")

  url             = models.URLField( 'Unprocessed URL', max_length=4096)
  url_referenced  = models.URLField( 'Referenced URL',  max_length=4096)
 
  dom_time   = models.IntegerField('Loading DOM time')  
  link_time  = models.IntegerField('Retreive links tIme')   
  event_time = models.IntegerField('Event time')  
  eval_time  = models.IntegerField('Evaluation time')   
  save_time  = models.IntegerField('Saving results time')   
  total_time = models.IntegerField('Total processing time')

  class Meta:
    verbose_name        = "URL: Unprocessed"
    verbose_name_plural = "URL: Unprocessed"
    ordering = ['url', 'url_referenced']

  def __unicode__(self):
    return self.url + " (" + self.url_referenced + ")" 

  def get_url(self):
    if len(self.url) > 50:
      return self.url[:50] + '...... '   
    else:
      return self.url   
     
  def get_reference_url(self):
    if len(self.url_referenced) > 50:
      return self.url_referenced[:50] + '...... '   
    else:
      return self.url_referenced  

# ---------------------------------------------------------------
#
# FilteredURL
#
# ---------------------------------------------------------------
  
class FilteredURL(models.Model):
  filtered_url_id = models.AutoField(primary_key=True)

  ws_report   = models.ForeignKey(WebsiteReport, related_name="filtered_urls")

  url            = models.URLField( 'Other URL',      max_length=4096)
  url_referenced = models.URLField( 'Referenced URL', max_length=4096)

  class Meta:
    verbose_name        = "URL: Filtered"
    verbose_name_plural = "URL: Filtered"
    ordering = ['url_referenced', 'url']

  def __unicode__(self):
    return self.url 

  def get_url(self):
    if len(self.url) > 50:
      return self.url[:50] + '...... '   
    else:
      return self.url   

  def get_domain(self):
    parsed = urlparse(self.url)
    
    return parsed.netloc   
      
     
  def get_reference_url(self):
    if len(self.url_referenced) > 50:
      return self.url_referenced[:50] + '...... '   
    else:
      return self.url_referenced

