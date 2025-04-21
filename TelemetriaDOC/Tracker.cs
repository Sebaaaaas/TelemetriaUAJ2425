using System;
using System.Collections.Generic;

namespace TelemetriaDOC
{
    public class Tracker
    {
        private static Tracker instance = null;
        private Serializer serializer;
        private Persistence persistence;

        private EventQueue eventQueue;

        private Guid sessionID;

        private Tracker()
        {
            // Para que los float se escriban siempre con "." en lugar de con ","
            System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo("en-US");
        }

        public static Tracker Instance()
        {
            return instance;
        }

        public static bool Init(Format format, Type type, string name, int sizeQueue)
        {
            if (instance != null)
                return false;

            instance = new Tracker();

            //Iniciar serializador
            instance.initSerializer(format);

            //Iniciar persistencia
            instance.initPersistence(type, name);

            instance.eventQueue = new EventQueue(ref instance, sizeQueue);

            instance.sessionID = Guid.NewGuid();

            return true;
        }

        public void initSerializer(Format format)
        {
            switch (format)
            {
                case Format.JSON:
                    instance.serializer = new SerializerJSON();
                    break;
            }
        }

        public void initPersistence(Type typeSave, string name)
        {
            switch (typeSave)
            {
                case Type.Disk:
                    instance.persistence = new DiskPersistence(name, instance.serializer);
                    break;
            }
        }

        public static void TrackEvent(Event e) 
        {
            e.setSessionID(instance.sessionID);
            instance.eventQueue.AddEvent(e);
        }

        public void flush(ref Queue<Event> events)
        {
            string text = "";

            // Serializamos cada evento de la cola
            while(events.Count > 0)
            {
                text += instance.serializer.serialize(events.Dequeue());
            }

            events.Clear();

            instance.persistence.write(text);            
        }

        public static void closing()
        {
            instance.CloseArch();
        }
        private void CloseArch()
        {
            instance.eventQueue.flushQueue();
            instance.persistence.write(instance.serializer.serializerEnding());
            instance.persistence.close();
        }
    }
}