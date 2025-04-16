using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public abstract class Event
    {
        string name;
        
        private Guid _id_session;
        private float _timestamp;

        public Event(float timestamp)
        {
            name = "Event";
            _timestamp = timestamp;
        }

        public virtual string getName() { return name; }
        public virtual string serializeToJSON()
        {
            string s = "    \"id\" :" + _id_session.ToString() + ",\n";
            s += "    \"timestamp\" : " + _timestamp;
            return s;
        }
        public void setSessionID(Guid sessionID) { _id_session = sessionID; }
    }
}
