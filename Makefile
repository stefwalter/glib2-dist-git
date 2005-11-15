# Makefile for source rpm: glib2
# $Id: Makefile,v 1.1 2004/08/31 10:08:53 cvsdist Exp $
NAME := glib2
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
