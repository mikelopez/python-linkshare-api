# -*- coding: utf-8 -*-
from lettuce import step, before, world
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals, assert_true

import sys, os
from settings import LS_API_HTTPGET_LOG, LS_API_HTTPRESPONSE_LOG, \
		LS_API_HTTPERRORS_LOG, BASE_API_LOGDIR

sys.path.append('lib/linkshare')
from LinkShareAPI2 import LinkShareAPI


@step(u'Given I instantiate "(.*)" with debug "(.*)"')
def given_i_instantiate_group1_with_debug_group2(step, classname, debug):
	world.raw_class = eval(classname)
	world.set_class = eval(classname)(debugbool=debug)
	assert_true(world.set_class)


@step(u'Class should contain "(.*)" method')
def class_should_contain_group1_method(step, attrname):
	assert_true(hasattr(world.set_class, attrname))

@step(u'Directory "(.*)" must exist')
def directory_group1_must_exist(step, dir):
	assert_true(os.path.exists(eval(dir)))

@step(u'Class should contain "(.*)"')
def class_should_contain_attrname(step, attrname):
	assert_true(hasattr(world.set_class, attrname))

@step(u'Variable "(.*)" should be "(.*)"')
def variable_group1_should_be_group2(step, varname, value):
	get_val = getattr(world.set_class, varname)
	assert_equals(get_val, value)

@step(u'The "(.*)" dictionary should contain "(.*)" key')
def the_group1_dictionary_should_contain_keyname_key(step, dict, keyname):
	get_val = getattr(world.set_class, dict)
	assert_true(keyname in get_val.keys())

@step(u'I set "(.*)" to "(.*)"')
def i_set_group1_to_group2(step, maxresults, value):
	world.set_class.urldata_dict[maxresults] = value
	assert_true(world.set_class.urldata_dict[maxresults], value)
	

@step(u'Then I search for "(.*)"')
def then_i_search_for_value(step, value):
	world.set_class.SetKeyword(value)
	assert True, "OK we set the keyword to %s" % (value)

@step(u'Then I construct the URL')
def then_i_construct_the_url(step):
	assert_true(world.set_class.ConstructURL())



@step(u'Then I should have logfile "(.*)"')
def then_i_should_have_logfile_group1(step, logfile):
	check_settings = False
	if eval(logfile) == LS_API_HTTPGET_LOG:
		check_settings = True
		assert_true(os.path.exists(LS_API_HTTPGET_LOG))
	if eval(logfile) == LS_API_HTTPRESPONSE_LOG:
		check_settings = True
		assert_true(os.path.exists(LS_API_HTTPRESPONSE_LOG))
	if eval(logfile) == LS_API_HTTPERRORS_LOG:
		check_settings = True
		assert_true(os.path.exists(LS_API_HTTPERRORS_LOG))
	assert_true(check_settings)

@step(u'The results list should have atleast one result')
def the_results_list_should_have_atleast_one_result(step):
	assert_true(len(world.set_class.product_results))

@step(u'The results dict should contain "(.*)" key')
def the_results_dict_should_contain_group1_key(step, group1):
	for i in world.set_class.product_results:
		assert_true(group1 in i.keys())
	assert True, "OK congradulations we can talk to Linkshare"

@step(u'Then I search for "(.*)"')
def then_i_search_for_something(step, something):
		assert_true(world.set_class.SetParameter('keyword', something))


@step(u'Then I fetch the data which constructs the url')
def then_i_fetch_the_data_which_constructs_the_url(step):
	world.set_class.FetchHTTP()
	assert True, "OK with HTTP"

	

@step(u'THen I process the parsed XML and return data')
def then_i_process_the_parsed_xml_and_return_data(step):
	assert_true(world.set_class.ProcessData())

