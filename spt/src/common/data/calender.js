var date = new Date();
var d = date.getDate();
var m = date.getMonth();
var y = date.getFullYear();
const calenderDefaultCategories = [
  {
    id: 1,
    title: "New Event Planning",
    type: "success",
    
  },
  {
    id: 2,
    title: "Meeting",
    type: "info",
  },
  {
    id: 3,
    title: "Generating Reports",
    type: "warning",
  },
  {
    id: 4,
    title: "Create New theme",
    type: "danger",
  },
];

export { calenderDefaultCategories};