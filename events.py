from collections import defaultdict
from datetime import datetime
import traceback

# =========================================
# EVENT BUS
# =========================================

class EventBus:

    def __init__(self):

        self.listeners = defaultdict(list)

        self.history = []

    # =====================================
    # SUBSCRIBE
    # =====================================

    def subscribe(
        self,
        event_name,
        callback
    ):

        self.listeners[event_name].append(
            callback
        )

    # =====================================
    # UNSUBSCRIBE
    # =====================================

    def unsubscribe(
        self,
        event_name,
        callback
    ):

        if (
            event_name
            in self.listeners
        ):

            if callback in self.listeners[event_name]:

                self.listeners[event_name].remove(
                    callback
                )

    # =====================================
    # EMIT
    # =====================================

    def emit(
        self,
        event_name,
        data=None
    ):

        event = {

            "time":
                str(datetime.now()),

            "event":
                event_name,

            "data":
                data
        }

        self.history.append(
            event
        )

        # ограничение истории

        if len(self.history) > 1000:

            self.history = self.history[-1000:]

        listeners = self.listeners.get(
            event_name,
            []
        )

        for callback in listeners:

            try:

                callback(data)

            except Exception:

                traceback.print_exc()

    # =====================================
    # GET HISTORY
    # =====================================

    def get_history(
        self,
        limit=50
    ):

        return self.history[-limit:]

# =========================================
# GLOBAL INSTANCE
# =========================================

event_bus = EventBus()