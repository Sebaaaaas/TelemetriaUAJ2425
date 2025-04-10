using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    class EventQueue
    {

        private Queue<Event> queue;
        private int max_size;

        EventQueue(int _max_size)
        {
            max_size = _max_size;
            queue = new Queue<Event>();
        }

        // Añade evento a la cola
        public void AddEvent(Event e)
        {
            // Si superamos el máximo de eventos, eliminamos el primero
            if(queue.Count >= max_size)
                queue.Dequeue();
            
            queue.Enqueue(e);   
        }


    }
}
