    def get_elasticsearch_thread_pool_status(self):
        """ Get elasticsearch thread pool status
        :return: dict where podname is the key and the pool status is the value.
            For example:
                {'logging-es-data-master-mz7182ko-2-drhts': {'bulk.queue': '0',
                                                             'bulk.rejected': '0',
                                                             'host': '10.131.2.16',
                                                             'bulk.completed': '1118756',
                                                             'bulk.active': '0',
                                                             'bulk.queueSize': '50'
                                                             },
                 'logging-es-data-master-cypn0g0h-2-9kpzb': {'bulk.queue': '0',
                                                             'bulk.rejected': '0',
                                                             'host': '10.128.2.12',
                                                             'bulk.completed': '729262',
                                                             'bulk.active': '0',
                                                             'bulk.queueSize': '50'
                                                             },
                 'logging-es-data-master-6lmw4rub-2-pxl4j': {'bulk.queue': '0',
                                                             'bulk.rejected': '0',
                                                             'host': '10.128.2.12',
                                                             'bulk.completed': '729262',
                                                             'bulk.active': '0',
                                                             'bulk.queueSize': '50'}
                 }
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """
        g.log.info("Getting elasticsearch thread pool states...")

        # Get elastic search pods

        obj_ops = OcpLoggingOperations()
        elasticsearch_pods = obj_ops.get_component_pods('es')

        # Get the queues rejected status
        elasticsearch_pods_thread_pool_status = {}
        for elasticsearch_pod in elasticsearch_pods:
            cmd = ("oc exec %s -n %s -- "
                   "curl -s -k --cert /etc/elasticsearch/secret/admin-cert "
                   "--key /etc/elasticsearch/secret/admin-key "
                   "https://localhost:9200/_cat/thread_pool?v\&h="
                   "host,bulk.completed,bulk.rejected,bulk.queue,bulk.active,"
                   "bulk.queueSize" %
                   (elasticsearch_pod, self.ocp_logging_project_name))
            ret, out, err = g.run(self.first_master, cmd)

            elasticsearch_pods_thread_pool_status[elasticsearch_pod] = {}
            if ret == 0 and out:
                
                _thread_pool_status = list(out.split("\n"))
                thread_pool_status = filter(None, _thread_pool_status)
                _fields = list(thread_pool_status[0].split())
                fields = filter(None,_fields )
                for each_status in thread_pool_status[1:]:
                    _each_status = list(each_status.split())
                    each_status = filter(None, _each_status)
                    for i in range(len(fields)):
                        (elasticsearch_pods_thread_pool_status[elasticsearch_pod][fields[i]]) = each_status[i]

                        g.log.info("Elasticsearch pods thread pool status:\n%s",
                   elasticsearch_pods_thread_pool_status)
        return elasticsearch_pods_thread_pool_status

    def are_elasticsearch_bulk_queues_rejected(self):
        """ Check if elasticseacrh bulk queues are rejected

        :return: bool. True if elasticsearch bluk queues are rejected.
            False otherwise.
        :raises: ocp_exceptions.ExecutionErrorn case of execution failures.
        """
        try:
            elasticsearch_pods_thread_pool_status = \
                self.get_elasticsearch_thread_pool_status()
        except ExecutionError as e:
            raise ExecutionError(e.message)

        _rc = False
        for pod in elasticsearch_pods_thread_pool_status:
            if int(elasticsearch_pods_thread_pool_status[pod]['bulk.rejected']) != 0:
                _rc = True
        return _rc
    
    
    
    
    
    #######################
    
     _out = list(set(out.split("\n")))
                elasticsearch_pods_indexes_state_dict_value = (list(filter(None, _out)))