# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/login_service_ss.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dprotos/login_service_ss.proto\"6\n\x10LoginCredentials\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\">\n\rLoginResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x12\n\x05token\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_token\"V\n\x11SignUpCredentials\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07surname\x18\x02 \x01(\t\x12\x10\n\x08username\x18\x03 \x01(\t\x12\x10\n\x08password\x18\x04 \x01(\t2k\n\x05Login\x12/\n\x08RpcLogin\x12\x11.LoginCredentials\x1a\x0e.LoginResponse\"\x00\x12\x31\n\tRpcSignUp\x12\x12.SignUpCredentials\x1a\x0e.LoginResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.login_service_ss_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOGINCREDENTIALS._serialized_start=33
  _LOGINCREDENTIALS._serialized_end=87
  _LOGINRESPONSE._serialized_start=89
  _LOGINRESPONSE._serialized_end=151
  _SIGNUPCREDENTIALS._serialized_start=153
  _SIGNUPCREDENTIALS._serialized_end=239
  _LOGIN._serialized_start=241
  _LOGIN._serialized_end=348
# @@protoc_insertion_point(module_scope)