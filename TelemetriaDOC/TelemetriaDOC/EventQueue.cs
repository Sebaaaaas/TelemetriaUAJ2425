using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class EventQueue
    {

        private Queue<Event> queue;
        private int max_size;
        private int numElems;

        public EventQueue(int _max_size)
        {
            max_size = _max_size;
            numElems = 0;
            queue = new Queue<Event>();
        }

        // Añade evento a la cola
        public void AddEvent(Event e)
        {
            // Si superamos el máximo de eventos, eliminamos el primero
            if(queue.Count >= max_size)
            {
                queue.Dequeue();
                numElems--;
            }
            
            queue.Enqueue(e);
            numElems++;
        }

        public int getNumElems() { return numElems; }
        public int getMaxSize() { return max_size; }

    }
}
