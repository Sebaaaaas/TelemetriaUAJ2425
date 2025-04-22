using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class EventQueue
    {
        Tracker tracker;

        private Queue<Event> queue;
        private int max_size;

        public EventQueue(ref Tracker tracker_, int _max_size)
        {
            max_size = _max_size;
            queue = new Queue<Event>();

            tracker = tracker_;
        }

        // Añade evento a la cola
        public void AddEvent(Event e)
        {
            queue.Enqueue(e);

            // Si superamos el máximo de eventos, vaciamos la cola
            if (queue.Count >= max_size)
            {                
                FlushQueue();
            }
        }
       
        public void FlushQueue()
        {
            tracker.Flush(ref queue);
        }

        public int GetMaxSize() { return max_size; }

    }
}