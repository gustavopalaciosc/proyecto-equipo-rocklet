import {useState} from "react"
import { IEvent } from "../interfaces/IEvent"


interface EventProps {
  event: IEvent;
  handleEventCheck: (event: IEvent) => void;
}

const Event : React.FC<EventProps> = ({ event, handleEventCheck }) => {
  const [isChecked, setIsChecked] = useState(false)
    const date = new Date(event.date)
    const datestring = date.toLocaleDateString()
  
    function onToggle() {
      console.log("checked")
      isChecked ? setIsChecked(false) : setIsChecked(true)
      handleEventCheck(event)
    }
  
    return (
      <div style={{display: "flex"}}>
        <input
          type="checkbox"
          checked={isChecked}
          onChange={onToggle}
        />
        <div>
          <label style={{ marginLeft: '8px' }}>{event.name}: {datestring}</label>
        </div>
      </div>
    );
  }

export { Event }

  