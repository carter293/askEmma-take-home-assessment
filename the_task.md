AI-Enhanced Incident Response System
Duration: 60 - 75 minutes
Objective:
Create a prototype system that processes social care call/meeting data, analyses it against
policies, and generates appropriate responses.
You have been provided with the mock transcript, policies document and incident form below.
You’ll also find these attached in .txt and .csv for ease of use.
Core Requirements:
●
Backend Development (Python/FastAPI):
○
Receiving transcript data from the front end.
○
Analysing the meeting data against the policies.
○
Generating an incident form based on the policies and template.
○
Draft an email to the appropriate person(s).
○
An OpenAI API key has been provided, use this at as many points as you see
appropriate.
○
Include fallback mechanisms & ease of fact checking.
●
Basic Next.js Frontend:
○
Inputting or pasting call/meeting data.
○
Displaying the generated incident form.
○
Showing the drafted email.
○
If you need to spend the time elsewhere, this can be completed through the
terminal rather than build the front end.
●
●
Code Quality and Documentation:
○
Include clear comments.
○
Implement error handling and logging.
Bonus (if time allows):
○
Allow the user to give feedback to the AI to edit generated content.
○
Suggest and briefly describe an innovative feature that could enhance the
incident response process.
Materials
Telephone Call Transcript
Julie Peaterson: "Good morning, Julie Peaterson speaking, how can I help you?"
Greg Jones: "Hi, uh, it's Greg... Greg Jones. I’ve, uh, I’ve fallen again.
"
Julie Peaterson: "Oh no, Greg! Are you alright? Where are you right now?"
Greg Jones: "I’m in the living room, on the floor... I tried getting up, but I just can’t seem to
manage it this time.
"
Julie Peaterson: "Okay, Greg, take a deep breath. Let’s not rush. Are you hurt? Do you feel any
pain or see any blood?"
Greg Jones: "No, no, there’s no blood... I don’t think anything's broken either. It’s just... I don’t
know. I feel a bit all over the place, to be honest. Can’t really remember how I ended up down
here.
"
Julie Peaterson: "Alright, that’s good to hear there’s no immediate injuries. But you sound a
little off. How long have you been on the floor, Greg?"
Greg Jones: "I don’t know... maybe 20 minutes? It could be longer. I just—my mind’s a bit
fuzzy, can’t really think straight right now.
"
Julie Peaterson: "Hmm, okay. You mentioned this has happened before. Has it been
happening often?"
Greg Jones: "Yeah, this is the third time... this week. I’m just so... so frustrated, Julie. Every
time I think I’m okay, and then... boom, I’m back on the floor.
"
Julie Peaterson: "Oh Greg, I’m really sorry to hear that. It must be so frustrating for you. Let’s
get you some help right away, okay? I’ll make sure someone gets to you as soon as possible.
"
Greg Jones: "Thanks, Julie. I just... I don’t know what’s going on anymore.
"
Julie Peaterson: "Don't worry, Greg. We’ll get this sorted, and we’ll talk about what’s been
happening. It sounds like we need to look at what’s going on a bit more closely.
"
Greg Jones: "Yeah, maybe... I just hate this feeling. I don’t want it happening again.
"
Julie Peaterson: "I completely understand, Greg. You’re doing great by calling in. We’ll get you
back on your feet and figure out how to prevent this from happening again.
"
Policies and Procedures
Section 1: Medication Administration
Medication management is an important aspect of care provision, and all carers must adhere to
proper procedures when administering medications.
●
●
●
●
●
Carers should check the service user’s care plan to ensure they understand the
medication schedule and dosage.
Confirm with the service user before administering any medication, and ensure they take
it as prescribed.
If a service user refuses medication, do not force them. Instead, document the refusal
and report it to your supervisor.
In cases where the service user appears confused or unaware of their medication
routine, notify the family and seek guidance.
Regular medication reviews should be scheduled, and any changes to prescriptions
must be updated in the care plan.
Section 2: First Aid and Emergency Response
Social care providers may encounter situations requiring basic first aid or emergency response.
●
Minor injuries such as cuts and scrapes should be cleaned and dressed following first
●
●
●
aid procedures.
In case of more serious injuries, such as suspected fractures, or if the service user is
unconscious, contact emergency services immediately.
In the event of bleeding or a medication overdose, carers should contact the service
user's GP immediately for further guidance.
If the GP is unavailable and the situation appears life-threatening, call 999 for urgent
medical support.
Section 3: Mobility & Moving
Falls are a common risk among service users and must be handled with immediate care and
attention to prevent further injury.
●
●
●
●
●
If a service user has fallen, first assess their physical state. Check for any signs of injury
such as bruising, cuts, or difficulty moving.
Ensure the service user is in a safe, comfortable position before attempting to assist
them.
If the service user can stand with support, help them to a chair or bed. If not, seek further
assistance from another carer.
If a service user falls, you must email your supervisor immediately with details of the
incident, including the time, location, and condition of the service user.
If this is a recurring issue (two or more falls in a week), cc the Risk Assessor on the
email and arrange for a moving and handling risk assessment review to address
potential hazards and ensure the service user’s environment is safe.
Section 4: Personal Care and Dignity
Maintaining the dignity and privacy of service users is essential in all personal care activities.
●
Always ensure privacy by closing doors and drawing curtains when providing personal
●
●
●
●
●
care.
Ask for the service user’s consent before beginning any personal care tasks and explain
what you are going to do.
Use proper personal protective equipment (PPE) to maintain hygiene and reduce
infection risks.
Respect the service user’s preferences for bathing, dressing, and other personal care
routines, ensuring they feel comfortable at all times.
If the service user expresses discomfort or refuses personal care, document the incident
and email your supervisor. If this happens more than once, also cc the service user’s
family for further support.
If PPE is unavailable during personal care, email your supervisor and document the
issue immediately.
Section 5: Mental Health and Emotional Well-being
Mental health is a critical component of overall well-being and should be monitored closely.
●
●
●
●
●
Carers should be aware of changes in a service user’s behaviour, including signs of
depression, anxiety, or withdrawal from social interactions.
Regularly check in with service users to ensure their emotional needs are being met.
If a service user expresses feelings of hopelessness, isolation, or distress, report this
immediately to the supervisor.
In cases where a service user calls in confused, disoriented, or excessively worried, alert
their family or next of kin to inform them of the situation and ensure appropriate follow-up
care can be arranged.
Support plans should include mental health considerations, and services users should
have access to mental health support if needed.
Section 6: Infection Control
Infection prevention is a key responsibility for all social care workers, especially when working
with vulnerable populations.
●
●
●
●
●
Always wash your hands before and after providing care to a service user.
Use PPE such as gloves, aprons, and masks, as appropriate for the task at hand.
Disinfect equipment and surfaces regularly, especially in shared living spaces.
If a service user is diagnosed with an infectious illness (e.g., flu, COVID-19), isolate them
according to guidance and report the case to your supervisor.
Follow proper waste disposal protocols for clinical waste, including dressings, gloves,
and other materials.
Section 7: Nutrition and Hydration
Ensuring that service users are well-nourished and hydrated is vital for their overall health and
well-being.
●
Carers should prepare and serve meals that meet the dietary needs and preferences of
service users, taking into account any allergies or medical conditions.
●
Offer fluids regularly to prevent dehydration, especially in warmer weather or if the
service user has difficulty communicating.
●
Document any significant changes in eating habits, such as a refusal to eat or a sudden
change in appetite, and report this to your supervisor.
●
For service users on a specialised diet (e.g., diabetic, low-sodium), ensure that all meals
adhere to the dietary guidelines provided.
Incident Report Form
Field Data Type
Date and Time of Incident DateTime
Service User Name Text field
Location of Incident Text field
Type of Incident Text field
Description of the Incident Text field
Immediate Actions Taken Text field
Was First Aid Administered? Boolean
Were Emergency Services
Contacted? Boolean
Who Was Notified? Text field
Witnesses Text field
Agreed Next Steps Text field
Risk Assessment Needed Boolean
If Yes, Which Risk
Assessment Text field