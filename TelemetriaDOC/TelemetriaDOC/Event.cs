using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public abstract class Event
    {
        string name;
        public Event() {
            name = "Event";
        }

        public virtual string getName() { return name; }
    }
}
