=====================
Django JOBS REST API 
=====================

This REST API is for posting and retrieving jobs to/from the django
community site. The intention is to allow sites that already have job
postings for django folks to cross-post them into the django community
site, and support django developers finding out about them either by
going to the django community site or by subscribing to the aggregated
job posts through a feed.

.. contents:: Contents

Overview
========

The API is based on django-piston and uses HttpBasicAuthentication, so
prior to using the API you will need to obtain a username/password for
the django community site. With the API (and appropriate credentials)
you can,

* Post new jobs.
* Update existing jobs.
* Delete jobs.
* List jobs.

To obtain credentials please do the following:

    1. <first step>
    2. <second step>
    
API Usage
=========

Authenticating
--------------

The django test code fragment below uses the django test client to
illustrate what you have to do to authenticate. It assumes you have
obtained credentials (described above) and will substitute
accordingly.

.. parsed-literal::

    import base64
    from django.test import TestCase
    
    class AuthTest(TestCase):
        def setUp(self):
            pass
        
        def testAuth(self):
            auth_string = 'Basic %s' % 
                base64.encodestring('username:password').rstrip()
            .
            .
            .
            response = self.client.get('/jobs',
                HTTP_AUTHORIZATION=auth_string)
       
        def tearDown(self):
            pass
    
If authentication fails, **<Insert Code Returned>** is returned.

Retrieving jobs
---------------

The example below retrieves all the job postings,

.. parsed-literal::

    -> GET /...        
            
    <- 200 Ok

Posting a new job
-----------------

The example below illustrates what you have to do to post a new
job. It assumes you have credentials to create a proper authentication
string as described above in {Authenticating_}.

.. parsed-literal::

    -> POST /...
            
    <- 201 Created

If authentication fails, **<Insert Code Returned>** is returned.
If the job posting fails, **<Insert Code Returned>** is returned.
If the job posting succeeds, **<Insert Code Returned>** is returned.
        
Deleting a job
-----------------

The example below illustrates what you have to do to delete a job. It
assumes you have credentials to create a proper authentication string
as described above in {Authenticating_}.

.. parsed-literal::

    -> DELETE /...
            
    <- 204 Empty

If authentication fails, **<Insert Code Returned>** is returned.
If the job deletion fails, **<Insert Code Returned>** is returned.
If the job deletion succeeds, **<Insert Code Returned>** is returned.
        
        
Updating an existing job
------------------------

The example below illustrates what you have to do to update an
existing job. It assumes you have credentials to create a proper
authentication string as described above in {Authenticating_}.

.. parsed-literal::

    -> PUT /...
            
    <- 200 Ok

If authentication fails, **<Insert Code Returned>** is returned.
If the update fails, **<Insert Code Returned>** is returned.
If the update succeeds, **<Insert Code Returned>** is returned.
        

