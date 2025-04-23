using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class EventQueue
    {
        public Queue<Event> queue;
        private int max_size;

        public EventQueue(int _max_size)
        {
            max_size = _max_size;
            queue = new Queue<Event>();
        }

        // Añade evento a la cola
        public void AddEvent(Event e)
        {
            queue.Enqueue(e);

            // Si superamos el máximo de eventos, eliminamos el primero
            if (queue.Count > max_size)
                queue.Dequeue();
        }

        public int GetMaxSize() { return max_size; }

    }
}