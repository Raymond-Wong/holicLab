def notify(request):
  # 待返回信息
  RET_STR = '<xml><return_code><![CDATA[%s]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>'
  print request.body
  return HttpResponse(RET_STR % ('SUCCESS', 'OK'))