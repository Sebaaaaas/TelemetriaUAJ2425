using System;
using System.Collections.Generic;
using System.Data;
using System.Text;

namespace TelemetriaDOC
{
    public abstract class Event
    {
        protected string name;
        
        private Guid _id_session;
        private float _timestamp;

        public Event(float timestamp)
        {
            name = "Event";
            _timestamp = timestamp;
        }

        public virtual string SerializeToJSON()
        {
            string s = "\"eventType\": \"" + name.ToString() + "\", ";
            s += "\"id\":\"" + _id_session.ToString() + "\", ";
            s += "\"timestamp\":" + _timestamp;
            return s;
        }
        public void SetSessionID(Guid sessionID) { _id_session = sessionID; }
    }
}
