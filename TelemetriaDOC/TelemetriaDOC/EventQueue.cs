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
            this.max_size = _max_size;
            queue = new Queue<Event>();
        }



    }
}
