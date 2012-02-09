# -*- encoding: utf-8 -*-
'''
Implement a general dependency map algorithm.

@author: pwx
@date: 2012-2-9
'''
from __future__ import unicode_literals, print_function, nested_scopes, division

# Please list all the modules you imported here for automatically reload.
from avalon.util import builtin
from avalon.util import object
_DEPENDENCY_ = [builtin, object]

# Dependency map
class MapNode(object.Object):
    '''
    Dependency map node.
    
    @ivar data: Node real data.
    @ivar targets: Node dependent targets.
    @ivar parents: Nodes that depend on this node.
    '''
    def __init__(self, data):
        self.data = data
        self.targets = []
        self.parents = []
        
    def toString(self):
        return 'data=%s, targets=%s, parents=%s' % (self.data, self.targets, self.parents)

class DependencyMap(object.Object):
    '''
    Dependency relation map.
    '''
    def __init__(self, get_dependency_proc):
        '''
        Create an empty map.
        
        @param get_dependency_proc: A function object to get dependency 
            relations from nodes. If target node is not a valid map node, 
            the function must return None; else it must return a valid 
            tuple or list, whether is is empty or not.
        '''
        if (not builtin.callable(get_dependency_proc)):
            raise ValueError('Param "get_dependency_proc" must be a function object.')
        self.nodes = {}
        self.fp = get_dependency_proc
        
    def remove(self, node):
        '''
        Remove an existing node from dependency map.
        
        @param node: Existing node.
        @raise: KeyError
        '''
        for n in self.nodes[node].parents:
            self.nodes[n].targets.remove(node)
        for n in self.nodes[node].targets:
            self.nodes[n].parents.remove(node)
        del self.nodes[node]
        
    def refresh(self):
        '''
        Re-calculate dependency relations of all nodes pushed.
        '''
        self.push(builtin.iterkeys(self.nodes))
        
    def push(self, nodes):
        '''
        Push nodes into dependency map. If node already exists, update its dependency.
        Only nodes mentioned in the parameter will be updated. For a global dependency 
        re-calculation, please use "refresh".
        
        @param nodes: Node collection, must be iterable.
        '''
        # create nodes
        target_jar = {}
        for n in nodes:
            targets = self.fp(n)
            if (targets is None):
                if n in self.nodes:
                    self.remove(n)
                continue
            target_jar[n] = targets
            self.nodes[n] = MapNode(n)
        # setup references
        for n in builtin.iterkeys(target_jar):
            # check target set
            targets = target_jar[n]
            targets_set = set([t for t in targets if t in self.nodes])
            # remove not alive old references
            old_targets_set = set(self.nodes[n].targets)
            for n2 in (old_targets_set - targets_set):
                self.nodes[n2].parents.remove(n)
                self.nodes[n].targets.remove(n2)
            # add new references
            for n2 in (targets_set - old_targets_set):
                self.nodes[n2].parents.append(n)
                self.nodes[n].targets.append(n2)
                
    def walk(self, proc, nodes=None):
        '''
        Walk on the dependency map and process each node. Nodes are iterated 
        according to dependency relations. Simple recursive implementation 
        for the time being, but may be use better methods later.
        
        Exceptions must be well handled in proc!
        
        @param proc: A function object to process each node.
        @param nodes: Start walk from initial nodes. Must be a collection.
            If None, then all nodes will be selected.
        '''
        memo = {}
        def loop(node, memo):
            for n in self.nodes[node].targets:
                if (n not in memo):
                    memo[n] = True
                    loop(n, memo)
                    proc(n)
        if (nodes is None):
            nodes = builtin.iterkeys(self.nodes)
        else:
            nodes = [n for n in nodes if n in self.nodes]
        for n in nodes:
            if (n not in memo):
                memo[n] = True
                loop(n, memo)
                proc(n)
                
