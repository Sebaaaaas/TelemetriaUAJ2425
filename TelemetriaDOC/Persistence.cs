using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public enum Type {Disk}
    public abstract class Persistence
    {
        public virtual void Write(string s) { }

        public virtual void Close() { }
    }
}
