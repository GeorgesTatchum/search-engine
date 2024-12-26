for $customer in /directory/customer
where not($customer/@id = /list/order/customer/@id)
return $customer/name
