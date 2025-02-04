<script>
    function showEvents(type) {
        fetch(`/events/filter/${type}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("event-list").innerHTML = data.events.map(event => 
                    `<li>${event.name} (${event.date})</li>`
                ).join("");
            });
    }
</script>

<div class="p-4 bg-white shadow-md rounded-lg cursor-pointer" onclick="showEvents('upcoming')">
    <h2 class="text-xl font-bold">Upcoming Events</h2>
    <p class="text-gray-500 text-2xl">{{ upcoming_events }}</p>
</div>
<div class="p-4 bg-white shadow-md rounded-lg cursor-pointer" onclick="showEvents('past')">
    <h2 class="text-xl font-bold">Past Events</h2>
    <p class="text-gray-500 text-2xl">{{ past_events }}</p>
</div>

<ul id="event-list" class="list-disc ml-6 mt-4"></ul>
