#!/bin/bash

a2enconf simplesamlphp
apache2ctl -D FOREGROUND
