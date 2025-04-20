using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public enum Format { JSON };
    interface Serializer
    {
        string serialize(Event e);
        string getExtension();

        string close();
    }
}
