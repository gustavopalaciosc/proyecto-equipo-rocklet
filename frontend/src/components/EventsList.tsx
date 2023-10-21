import { useState } from 'react'
import { Event } from './Event'
import { IEvent } from '../interfaces/IEvent'

interface EventsListProps {
  events: IEvent[];
  handleSelectedEventsChange: (events: IEvent[]) => void;
}

const EventsList : React.FC<EventsListProps> = ({events, handleSelectedEventsChange}) => {

  const [selectedEvents, setSelectedEvents] = useState<IEvent[]>([])

  const handleEventCheck = (event: IEvent) => {
    console.log(`Event: ${event.id} changed`)
    let newMarkedEvents: IEvent[]
    if (selectedEvents.includes(event)) {
      newMarkedEvents = selectedEvents.filter((event_) => event_.id !== event.id)
    } else {
      newMarkedEvents = [...selectedEvents, event]
    }
    setSelectedEvents(newMarkedEvents)
    handleSelectedEventsChange(newMarkedEvents)
  }

  return (
    <div style={{display: 'flex', flexDirection: "column", alignItems: "center"}}>
      <div>
        {events.map((event) => (<Event key={event.id} event={event}  handleEventCheck={handleEventCheck}></Event>))}
      </div>
    </div>
  )
}

export {EventsList}