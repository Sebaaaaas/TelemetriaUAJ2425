using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public abstract class Event
    {
        string name;
        private int _id_session;
        private float _timestamp;
        public Event(int id_session,float timestamp) {
            name = "Event";
            _id_session = id_session;
            _timestamp = timestamp;
        }

        public virtual string getName() { return name; }
        public virtual string serializeToJSON()
        {
            string s = "    \"id\" :" + _id_session + ",\n";
            s += "    \"timestamp\" : " + _timestamp;
            return s;
        }
    }
}
