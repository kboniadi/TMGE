from typing import Set

from src.listener.iobserver import IObserver
from src.listener.isubscriber import ISubscriber


class Event:
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name
    
class QuitEvent(Event):
    def __init__ (self):
        self.name = "Quit event"

class TickEvent(Event):
    def __init__ (self):
        self.name = "Tick event"
    
    
class InputEvent(Event):
    def __init__(self, unicodechar, clickpos, event=None):
        self.name = "Input event"
        self.char = unicodechar
        self.clickpos = clickpos
        self.event = event
    def __str__(self):
        return '%s, char=%s, clickpos=%s' % (self.name, self.char, self.clickpos)
    
class InitializeEvent(Event):
    def __init__ (self):
        self.name = "Initialize event"

class StateChangeEvent(Event):
    def __init__(self, state):
        self.name = "State change event"
        self.state = state
    def __str__(self):
        if self.state:
            return '%s pushed %s' % (self.name, self.state)
        else:
            return '%s popped' % (self.name, )

class EventManagerWeak:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.cache = WeakKeyDictionary()

    def register(self, observer):
        if not isinstance(observer, IObserver):
            raise NotImplementedError("observer object must implement IObserver class")
        self.cache[observer] = 1

    def unregister(self, observer):
        if observer in self.cache:
            del self.cache[observer]
        
    def notify(self, event: 'Event'):
        if not isinstance(event, TickEvent):
            pass
            # print the event (unless it is TickEvent)
            # print(str(event))
        for obs in self.cache:
            obs.update(event)
    
    def clear(self):
        self.cache.clear()

class EventManager:
    def __init__(self):
        self.dict = dict()

    def register(self, subscriber, observer):
        if not isinstance(subscriber, ISubscriber):
            raise NotImplementedError("subscriber object must implement ISubscriber class")
        if not isinstance(observer, IObserver):
            raise NotImplementedError("observer object must implement IObserver class")
        
        if subscriber not in self.dict:
            self.dict[subscriber] = set()
        self.dict[subscriber].add(observer)

    def unregister(self, subscriber, observer):
        if not isinstance(subscriber, ISubscriber):
            raise NotImplementedError("subscriber object must implement ISubscriber class")
        if not isinstance(observer, IObserver):
            raise NotImplementedError("observer object must implement IObserver class")
        
        obs_ref: Set[IObserver] = self.dict.get(subscriber, None)
        if obs_ref is not None:
            obs_ref.remove(observer)

            if len(obs_ref) == 0:
                del self.dict[subscriber]
        
    def notify(self, subscriber, event):
        if not isinstance(subscriber, ISubscriber):
            raise NotImplementedError("subscriber object must implement ISubscriber class")
        
        if subscriber not in self.dict:
            return

        obs_ref: Set[IObserver] = self.dict.get(subscriber, None)
        if obs_ref is not None:
            for obs in obs_ref:
                obs.update(event)
    
    def remove_all_observer(self, subscriber):
        if not isinstance(subscriber, ISubscriber):
            raise NotImplementedError("subscriber object must implement ISubscriber class")

        if subscriber in self.dict:
            del self.dict[subscriber]
    
    def has_observers(self, subscriber):
        if not isinstance(subscriber, ISubscriber):
            raise NotImplementedError("subscriber object must implement ISubscriber class")

        return self.dict.get(subscriber, None) != None

    def clear(self):
        self.dict.clear()
