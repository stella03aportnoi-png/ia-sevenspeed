import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA Sevenspeed", page_icon="🏎️", layout="wide")

# Cabeçalho
st.title("🏎️ Chatbot Oficial Sevenspeed")
st.markdown("""
Bem-vindo! Sou a inteligência artificial da equipe **Sevenspeed**. 
Estou treinada com:
* Regulamentos Técnicos e de Competição (2025)
* Regras do Projeto Social
* Guia de Gestão de Projetos (PMIEF)
""")

# --- CONFIGURAÇÃO DA API (CÉREBRO) ---
# O Streamlit vai buscar a senha nos "Secrets" do servidor
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Erro de Configuração: Não encontrei a chave da API. Se você é o dono do site, verifique os 'Secrets' no painel do Streamlit.")
    st.stop()

# --- BASE DE CONHECIMENTO (SEUS DOCUMENTOS) ---
# Aqui estão todos os textos que você enviou, organizados.
base_de_conhecimento = """
Finals 2022 Technical Regulations
©2025 – STEM Racing Ltd. Page 1 of 58 24 July 2025
57
Front Cover – Team Hydron, Australia, 2022 World Champions and the new Technical Regulations car for 2025.
REVISION 2
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 2 of 58 24 July 2025
Front Cover – evolut1on, Germany, Aramco STEM Racing™ 2024 World Champions
CONTENTS
TECHNICAL REGULATIONS...............................................................................................................................................................5
HELP TEXT ..........................................................................................................................................................................................5
LIST OF REVISIONS 1:........................................................................................................................................................................5
LIST OF REVISIONS 2:........................................................................................................................................................................5
ARTICLE T1 – DEFINITIONS ...............................................................................................................................................................7
T1.1 STEM RACING™ CAR......................................................................................................................................7
T1.2 FULLY ASSEMBLED CAR.....................................................................................................................................8
T1.3 BODY..............................................................................................................................................................8
T1.4 POWER UNIT CARTRIDGE CHAMBER ....................................................................................................................8
T1.5 WING..............................................................................................................................................................9
T1.6 WING SUPPORT STRUCTURE AND END PLATE .....................................................................................................10
T1.7 NOSE CONE...................................................................................................................................................10
T1.8 WHEEL..........................................................................................................................................................10
T1.9 WHEEL SUPPORT SYSTEM ...............................................................................................................................10
T1.10 TETHER LINE GUIDE ........................................................................................................................................10
T1.11 SURFACE FINISH AND DECALS ..........................................................................................................................10
T1.12 STEM RACING™ LOGO DECAL........................................................................................................................11
T1.13 HAND FINISHING .............................................................................................................................................11
T1.14 OFFICIAL STEM RACING™ MODEL BLOCK ....................................................................................................11
T1.15 ENGINEERING DRAWINGS ................................................................................................................................11
T1.16 RENDERINGS .................................................................................................................................................12
T1.17 REFERENCE PLANES ......................................................................................................................................12
T1.18 ADDITIONAL COMPONENTS..............................................................................................................................13
T1.19 NORMAL........................................................................................................................................................13
T1.20 FULL 8 GRAM POWER UNIT CARTRIDGE .............................................................................................................13
T1.21 HALO ............................................................................................................................................................14
T1.22 LEGAL BALLAST .............................................................................................................................................14
ARTICLE T2 – GENERAL PRINCIPLES ............................................................................................................................................15
T2.1 REGULATIONS DOCUMENTS .............................................................................................................................15
T2.2 INTERPRETATION OF THE REGULATIONS ............................................................................................................15
T2.3 AMENDMENTS TO THE REGULATIONS ................................................................................................................15
T2.4 CLASSIFICATION OF REGULATIONS ...................................................................................................................15
T2.5 COMPLIANCE WITH REGULATIONS.....................................................................................................................15
T2.6 DESIGN IDEAS AND REGULATION COMPLIANCE QUESTIONS ..................................................................................16
T2.7 MEASUREMENTS ............................................................................................................................................16
T2.8 BENEFIT OF DOUBT.........................................................................................................................................16
T2.9 SPIRIT OF THE COMPETITION............................................................................................................................17
T2.10 ORIGINALITY OF WORK ...................................................................................................................................17
ARTICLE T3 – FULLY ASSEMBLED CAR.........................................................................................................................................19
T3.1 DESIGN AND MANUFACTURE – [GENERAL | PENALTY – 5PTS EACH]...................................................................19
T3.2 SAFE CONSTRUCTION [SAFETY | PENALTY – 10PTS EACH]...............................................................................19
T3.3 DEFINED FEATURES – [PERFORMANCE | PENALTY – 20PTS]..........................................................................19
T3.4 TOTAL WIDTH – [GENERAL | PENALTY – 5PTS PER MILLIMETRE]........................................................................19
T3.5 TOTAL HEIGHT – [GENERAL | PENALTY – 5PTS PER MILLIMETRE] ......................................................................19
T3.6 TOTAL WEIGHT – [PERFORMANCE | PENALTY – 10PTS PER GRAM] .................................................................20
T3.7 TRACK CLEARANCE – [GENERAL | PENALTY – 10PTS PER MILLIMETRE] .............................................................20
T3.8 STATUS DURING RACING - [GENERAL | PENALTY – 5PTS].................................................................................20
T3.9 REPLACEMENT COMPONENTS [GENERAL]......................................................................................................20
ARTICLE T4 – BODY .........................................................................................................................................................................22
T4.1 BODY CONSTRUCTION – [GENERAL | PENALTY – 20PTS] .................................................................................22
T4.2 VIRTUAL CARGO – [PERFORMANCE | PENALTY – 25PTS]...............................................................................22
T4.3 VIRTUAL CARGO IDENTIFICATION – [GENERAL | PENALTY – 5 PTS] ....................................................................22
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 3 of 58 24 July 2025
T4.4 HALO ............................................................................................................................................................23
T4.5 HELMET – [GENERAL | PENALTY – 5PTS] .......................................................................................................24
T4.6 STEM RACING™ LOGO DECAL LOCATION – [GENERAL | PENALTY – 5PTS]........................................................25
T4.7 TEAM NUMBER – [GENERAL | PENALTY – 2PTS] .............................................................................................25
T4.8 DECAL THICKNESS – [GENERAL | PENALTY – 5PTS] ........................................................................................25
ARTICLE 5 – POWER UNIT CARTRIDGE CHAMBER.......................................................................................................................26
T5.1 DIAMETER – [SAFETY | PENALTY – 5PTS] .......................................................................................................26
T5.2 DISTANCE FROM TRACK SURFACE – [GENERAL | PENALTY – 5PTS PER MILLIMETRE] ...........................................26
T5.3 DEPTH – [SAFETY | PENALTY – 5PTS] ............................................................................................................26
T5.4 MAX ANGLE OF CHAMBER – [SAFETY | PENALTY – 5PTS] .................................................................................26
T5.5 CHAMBER SAFETY ZONE – [SAFETY | PENALTY – 10PTS]..................................................................................26
T5.6 POWER UNIT CARTRIDGE VISIBILITY – [PERFORMANCE | PENALTY – 10PTS PER MILLIMETRE] ............................27
ARTICLE T6 – TETHER LINE GUIDES ..............................................................................................................................................28
T6.1 LOCATION – [SAFETY | PENALTY – 10PTS]......................................................................................................28
T6.2 INTERNAL DIMENSION – [SAFETY | PENALTY – 5PTS]........................................................................................28
T6.3 TETHER LINE GUIDE SAFETY – [SAFETY | PENALTY – 10PTS] ............................................................................29
ARTICLE T7 – WHEELS AND WHEEL SUPPORT STRUCTURES ...................................................................................................30
T7.1 NUMBER AND LOCATION – [GENERAL | PENALTY – 25PTS]...............................................................................30
T7.2 DISTANCE BETWEEN OPPOSING WHEELS – [PERFORMANCE | PENALTY – 2.5PTS PER MILLIMETRE PER AXLE]......30
T7.3 WHEELBASE – [PERFORMANCE | PENALTY –5PTS PER MILLIMETRE] ...............................................................30
T7.4 TRACK CONTACT WIDTH – [PERFORMANCE | PENALTY – 2.5PTS PER MILLIMETRE PER WHEEL] ..........................31
T7.5 DIAMETER – [PERFORMANCE | PENALTY – 2.5PTS PER MILLIMETRE PER WHEEL] .............................................31
T7.6 RACE TRACK CONTACT – [PERFORMANCE | PENALTY – 2.5PTS PER WHEEL]....................................................31
T7.7 ROLLING SURFACE – [PERFORMANCE | PENALTY – 2.5PTS PER WHEEL] .........................................................31
T7.8 ROTATION – [PERFORMANCE | PENALTY – 5PTS PER WHEEL] ........................................................................31
T7.9 VISIBILITY IN TOP AND BOTTOM VIEWS – [PERFORMANCE]..............................................................................32
T7.10 VISIBILITY IN SIDE VIEWS – [PERFORMANCE | PENALTY – 10PTS PER WHEEL] ..................................................33
T7.11 VISIBILITY IN FRONT VIEW – [PERFORMANCE | PENALTY – 10PTS PER MILLIMETRE] ..........................................33
T7.12 WHEEL SUPPORT – [GENERAL | PENALTY – 5PTS EACH]..................................................................................33
T7.13 WHEEL SAFETY TEST [SAFETY | PENALTY – 2.5PTS PER WHEEL].......................................................................34
ARTICLE T8 – NOSE, FRONT WING, END PLATES AND WING SUPPORT STRUCTURES...........................................................35
T8.1 NOSE, FRONT WING, END PLATES AND WING SUPPORT STRUCTURE IDENTIFICATION – [GENERAL | PENALTY – 5PTS]35
T8.2 NOSE CONE ASSEMBLY DIMENSION - [GENERAL | PENALTY – 5PTS EACH]..........................................................35
T8.3 FRONT WING(S) DESCRIPTION AND PLACEMENT – [GENERAL | PENALTY – 5PTS] ...................................................35
T8.4 FRONT WING(S) CONSTRUCTION AND RIGIDITY – [GENERAL | PENALTY – 5PTS].....................................................35
T8.5 NOSE, FRONT WING(S), FRONT WING END PLATES AND WING SUPPORT LOCATION ..................................................36
T8.6 FRONT WING DIMENSIONS – [PERFORMANCE].............................................................................................38
T8.7 FRONT WING CLEAR AIRFLOW - [PERFORMANCE | PENALTY – 5PTS] ...............................................................40
T8.8 FRONT WING VISIBILITY – [PERFORMANCE | PENALTY – 10PTS] .....................................................................40
ARTICLE T9 – REAR WING AND WING SUPPORT STRUCTURES. ................................................................................................41
T9.1 REAR WING AND WING SUPPORT STRUCTURE IDENTIFICATION – [GENERAL | PENALTY – 5PTS]................................41
T9.2 REAR WING DESCRIPTION AND PLACEMENT – [GENERAL | PENALTY – 5PTS] .........................................................41
T9.3 REAR WING CONSTRUCTION AND RIGIDITY – [GENERAL | PENALTY – 5PTS]...........................................................41
T9.4 REAR WING, WING SUPPORT STRUCTURE AND REAR OVERHANG LOCATION ...........................................................41
T9.5 REAR WING DIMENSIONS – [PERFORMANCE]................................................................................................42
T9.6 REAR WING CLEAR AIRFLOW – [PERFORMANCE | PENALTY – 5PTS] ................................................................44
T9.7 REAR WING VISIBILITY – [PERFORMANCE | PENALTY – 10PTS] .......................................................................45
ARTICLE T10 – ADDITIONAL COMPONENTS..................................................................................................................................45
T10.1 DESCRIPTION AND PLACEMENT [GENERAL] ....................................................................................................45
APPENDIX – OTHER INFORMATION & ILLUSTRATIONS ...............................................................................................................47
I. START BOX AND FINISH GATE ......................................................................................................................................47
II. OFFICIAL STEM RACING™ MODEL BLOCK DIMENSIONS................................................................................................48
III. FRONT WING COMPLIANCE EXAMPLES ..........................................................................................................................49
IV. REAR WING COMPLIANCE EXAMPLES............................................................................................................................51
V. WING OVERLAP .........................................................................................................................................................53
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 4 of 58 24 July 2025
VI. OFFICIAL DENFORD RACE POWER PACK DIMENSIONS...................................................................................................54
VII. CAR DECELERATION SYSTEM ....................................................................................................................................54
VIII. EXAMPLE OF COMPONENT IDENTIFICATION..................................................................................................................55
IX. HALO AND BALLAST CONTAINER DRAWINGS..................................................................................................................56
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 5 of 58 24 July 2025
Please note: any amendments made prior to the event will be indicated using red underlined text.
TECHNICAL REGULATIONS
Please read the whole document without assumptions from previous rules documents.
HELP TEXT
When you see green italic text, this is intended to help clarify a regulation or diagram.
When you see the PP+ symbol in the margin, this means a rule carries a Proportional Penalty. Find out more
about Proportional Penalties and the classification of rules in T2.5.
LIST OF REVISIONS 1:
T1.1 – Updated diagram
T1.12 – Updated examples
T3.1.3 – Updated wording
T3.5 – Amended diagram
T4.7 – Wording updated
T9.5.2 - Amended diagram
LIST OF REVISIONS 2:
T1.21 - Updated with part reference
T1.22 - Updated wording
T3.9 - Replacement Components - Updated to include tether guides
T4.4.1 Updated with part reference
T4.5 - Updated with part reference
T5.6 - Updated wording
ix. Halo and Ballast container drawings - Updated wording & new Diagram
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 6 of 58 24 July 2025
Definitions: 07
General Principles: 15
Car Design: Compliance & Penalties: 18
Appendix: 46
REGULATIONS
TECHNICAL
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 7 of 58 24 July 2025
ARTICLE T1 – DEFINITIONS
T1.1 STEM Racing™ car
This is also referred to as ‘the car’. Designed and manufactured according to these regulations for the
purpose of participating in races on the STEM Racing™ track at the World Finals event, powered only
by a single 8 grams power unit cartridge. STEM Racing™ cars are designed to travel the 20-metre race
and withstand the physical deceleration required after crossing the finishing line.
A STEM Racing™ car assembly must only consist of the following components:
Adhesives with no dimensional impact are permissible for joining components.
Example parts:
1. A body encompassing a virtual cargo and a power unit cartridge
chamber machined from a single piece of STEM Racing™ Model
Block Material
2. Nose cone assembly (Optionally Replaceable)
o Front wing support structure
o Front wing(s)
o End plates
3. Rear Wing Assembly
o Rear wing support structure
o Rear wing(s)
o End plates
4. Front wheel support system(s)
o Front wheel(s) rotating.
o Wheel support structure non rotating
5. Rear wheel support system(s)
o Rear wheel(s) rotating.
o Wheel support structure non rotating
6. Front tether line guide
12
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 8 of 58 24 July 2025
7. Rear tether line guide
8. Surface finishing and decals
9. STEM Racing™ Logo Decal (2)
10. Halo
11. Drivers Helmet
12. Legal Ballast
Refer to T1.22 and T4 for more information

T1.2 Fully assembled car
A STEM Racing™ car, without a power unit cartridge inserted, presented ready for racing, resting on all
four wheels on the track surface, free of any external force other than gravity.
T1.3 Body
The body is a single uninterrupted piece of STEM Racing™ Model Block material existing rear of
reference plane A and encompassing both the virtual cargo and power unit cartridge chamber. For
dimensional purposes the body also includes any attached decals and surface finishes. Any STEM
Racing™ Model Block forward of reference plane A is not defined as body.
T1.4 Power unit cartridge chamber
The power unit cartridge chamber is a cylindrical clear space bounded around its inner circumference
and forward end by car body only. This is where the power unit cartridge is placed for racing.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 9 of 58 24 July 2025
T1.5 Wing
A wing on a STEM Racing™ car is an aerodynamic feature that permits airflow around its minimum
required chord surface including its features of a leading and trailing edge across its minimum required
span width. A wing is dimensionally defined by the span, chord and thickness. The vertical crosssectional shape of the wing, parallel to the direction of car travel, is referred to as an aerofoil.
Wing cross-section / aerofoil naming terminology:
Wing naming terminology applied to single vane wing
Wing naming terminology applied to multiple vane wing


Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 10 of 58 24 July 2025
T1.6 Wing support structure and end plate
T1.6.1 Front Wing support Structure
Front wing support structure is a feature forward of reference plane A, that joins a wing(s) to the nose
cone.
T1.6.2 Rear Wing support Structure
Rear wing support structure is a feature rearward of reference plane B, that joins the wing to the car
body.
T1.6.3 End Plate
Any structure that forms part of a wing assembly outside of the minimum wing span.
T1.7 Nose cone
The nose cone is a component of the car, which is used as a wing support structure, that only exists
forward of reference plane A. This includes any STEM Racing™ Model Block material or any other
materials that continue forward of reference plane A.
T1.8 Wheel
A wheel is a single part or assembly of components, cylindrical in form, with its maximum circumference
contacting the track surface, allowing forward motion of the car through rotation.
T1.9 Wheel support system
Wheel support systems are single parts or an assembly of components that connect a wheel to any
other part of the car, they MUST be contained within a theoretical cylindrical extrusion defined by the
actual diameter of the relative wheels across each axle. These may be sourced from a supplier or
manufactured wholly or in part by the team.
T1.10 Tether line guide
A tether line guide is a key safety component which completely surrounds the track tether line so as to
safely connect the car to the tether line during races. A tether line guide can be a component sourced
from a supplier or manufactured wholly or in part by the team.
T1.11 Surface finish and decals
A surface finish on an STEM Racing™ car is considered to be any applied visible surface covering, of
uniform thickness over the profile of an STEM Racing™ car assembly component. A decal is material
adhered to a component or surface finish. To be defined as a decal, 100% of the area of the adhering
side must be attached to a surface. Surface finishes and decals are included when measuring the
dimensions of any components they feature on.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 11 of 58 24 July 2025
T1.12 STEM Racing™ logo decal
Teams must use a labelled decal to identify Car A and Car B and a blank decal to identify display car(s).
The official decals are supplied by STEM Racing Limited at event registration.
This consists of the STEM Racing™ logo graphic printed on a black or a white adhesive vinyl with a
1mm contrast keyline border, with a horizontal dimension of 30mm and vertical dimension of 15mm.
Teams choose to use either the black or white outlined decal so as to provide maximum contrast to the
surface colour the decal is being adhered to.
A team can manufacture and fit their own decals, provided they use the official STEM Racing™ logo
decal artwork, which can be downloaded from the STEM Racing™ website:
https://www.stemracing.com/downloads.html
Decal designs:
T1.13 Hand finishing
Hand finishing is defined as use of a hand powered device (e.g. abrasive paper) for removing only the
irregularities that may remain on a CNC machined surface of the car body. These irregularities are often
referred to as ‘machined marks’, any hand finishing must be kept to a minimum.
T1.14 Official STEM RACING™ Model Block
The official STEM Racing™ Model Block Material is a rigid, closed cell foam block processed to the
dimensional features as shown by diagrams in the appendix of this document.
IMPORTANT: all cars entered into the Aramco STEM Racing™ World Finals 2025 must be
manufactured from STEM RACING™ Model Blocks. The official STEM RACING™ Model Blocks can be
sourced directly from Denford Limited or an official Denford Limited distributor.
T1.15 Engineering drawings
Engineering drawings are CAD produced drawings which should be detailed such that, along with
relevant CAM programs, could theoretically be used to manufacture the fully assembled car by a third
party. Such drawings MUST include all relevant dimensions and material information.
Where stated, STEM Racing™ engineering drawings of a readable scale MUST be clearly dimensioned
and identified by hatching, shading, block colour or boundary line within the engineering drawings
to specifically identify and prove compliance for the virtual cargo, front and rear wheel support
structures, nose, front and rear wing support structures and front and rear wing surfaces.
Clearly labelled construction or boundary lines are acceptable to define the boundaries between
components such as nose cone, wheel support and wing support structures.
Engineering drawings can include: orthographic projection, auxiliary projection, section views, isometric
projection, oblique projection, perspective and annotated renderings.
It is recommended to label the relevant technical regulations where appropriate (e.g T9.5.1: 25.0mm)
throughout your Engineering drawings; this makes the job of the scrutineer much easier in identifying
the different features of your car.
See competition regulations scorecard for mandatory detailed list.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 12 of 58 24 July 2025
T1.16 Renderings
Renderings are images intended to illustrate the three-dimensional form of an object. These can be
generated in isometric projection, oblique projection, or perspective.
T1.17 Reference Planes
T1.17.1 Vertical Reference Plane
To assist with describing dimensions, it is assumed that a two-dimensional invisible plane exists along
the length of the power unit cartridge chamber centre axis and normal to the track surface. This is
known as the vertical reference plane.
T1.17.2 Reference Plane A
To assist with describing dimensions, it is assumed that a two-dimensional invisible plane exists
16.0mm in front of the front axle centre line normal to the track surface. This is known as reference
plane A.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 13 of 58 24 July 2025
T1.17.3 Reference Plane B
To assist with describing dimensions, it is assumed that a two-dimensional invisible plane exists
16.0mm to the rear of the rear axle centre line normal to the track surface.
This is known as reference plane B.
T1.18 Additional Components
Any component other than those listed in T1.1 will be considered an additional component.
T1.19 Normal
The term ‘normal’ can be used in geometry to describe a line or object that is perpendicular or at 90
degrees to another given object. When referring to the term normal in these regulations it is considered
to mean:
a. Being at right angles; perpendicular.
b. Perpendicular to the direction of a tangent line of a curve or a tangent plane to a surface.
T1.20 Full 8 gram power unit cartridge
A metallic cartridge which contains an 8 gram charge of compressed air. For weights and dimensions
refer to appendix v. Official Denford Race Power Pack dimensions.


Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 14 of 58 24 July 2025
T1.21 Halo
The halo is a driver crash-protection system used in open-wheel racing series, which consists of a
curved bar placed to protect the driver's head. The Halo is being introduced to STEM Racing™ not only
to echo real Formula 1® car design but also as a component of a new car deceleration system.
The Halo (halo_2025_with_6mm_hole_and_sr_logo) is available to download as a universal 3D part
from the STEM Racing™ website. For this part and more free downloads, please visit
https://www.stemracing.com/downloads.html
The Halo MUST be included in the final car design. Detailed Engineering Drawings are available in
appendix ix.
The Halo must be well adhered to the body of the car, to achieve this requires a recess or pocket to
match the underside of the Halo in the car body. It has been designed so the required recess or pocket
can be manufactured using a 1/4" (6.35mm) or smaller ball nose cutter. The Halo and the Helmet are
mandatory items and can be made from any material. Please refer to T4.4 for the halo file. Please see
Appendix ix for further details.
T1.22 Legal Ballast
To help achieve the minimum weight, legal ballast may now be added only to the container under the
halo, accessible through the halo/helmet aperture (hole). This is the only permitted location for ballast.
The ballast can consist of materials such as fishing lead weights or similar.
Using legal ballast is optional but strongly recommended, as it is the only legal method for adding
additional weight to meet the minimum weight requirement.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 15 of 58 24 July 2025
ARTICLE T2 – GENERAL PRINCIPLES
T2.1 Regulations documents
T2.1.1 STEM Racing Limited, issues the regulations, their revisions and amendments made.
T2.1.2 Technical Regulations - this document. The Technical Regulations document is mainly
concerned with those regulations that are directly related to STEM Racing™ car design and
manufacture. Technical regulation article numbers have a ‘T’ prefix.
T2.1.3 Competition Regulations – a document separate to this one which is mainly concerned with
regulations and procedures directly related to judging and the competition event. Competition
Regulation article numbers have a ‘C’ prefix.
T2.2 Interpretation of the regulations
T2.2.1 The final text of these regulations is in English should any dispute arise over their interpretation.
The text of a regulation and any related definitions should be considered together for the purpose of
interpretation.
IMPORTANT: Diagrams and or images are for illustration purposes only and do not contribute to
regulatory compliance.
T2.2.2 Text clarification - any questions received that are deemed by STEM Racing Limited to be
related to regulation text needing clarification will be answered by STEM Racing Limited The question
received, along with the clarification provided by STEM Racing Limited, will be published to all
competing teams at the same time via the official STEM Racing™ website:
https://www.stemracing.com/clarifications-2025.html
T2.3 Amendments to the regulations
Any amendments will be announced and released by STEM Racing Limited by email notification to all
In-Country Coordinators (ICC) as well as being posted on the website www.stemracing.com
Any amended text will be indicated thus (using red underlined text).
T2.4 Classification of regulations
T2.4.1 The technical regulations are classified as either: GENERAL, SAFETY, PERFORMANCE.
GENERAL SAFETY PERFORMANCE
Regulations that shape the way
the car fundamentally looks and
works, vital to the style of an
STEM Racing™ car.
Mandatory rules that govern the
safe running of the car. Cars
must meet these rules to be
considered ‘safe to race’.
Rules that have a direct impact
on the performance of the
vehicle, these typically carry the
heaviest penalties.
T2.4.2 If a race car is judged as being NON-COMPLIANT with any Performance regulation they will
be INELIGIBLE for the awards of: ‘Fastest Car’ and ‘Best Engineered Car’. All Performance
regulations are highlighted in yellow throughout this document.
T2.5 Compliance with regulations
T2.5.1 Points are deducted for non-compliance with the technical regulations as per the penalties as
defined in this document. Both race cars are assessed during Specification Judging and points will be
deducted for any infringements on either car. These penalties are only applied once, per infringement,
per car.
After initial Specification Judging any team with “safety” infringements will be given a single 20 minute
car service session. See competition regulations for more information.
T2.5.2 Proportional penalties will be applied to the following regulations:
T3.4, T3.5, T3.6, T3.7, T5.2, T5.6, T7.2, T7.3, T7.4, T7.5, T7.11, T8.6, T8.6.2, T8.6.3, T9.5.1, T9.5.2,
T9.5.3, T9.5.4
The penalty applied increases proportionally as the margin of non-compliance with the absolute
minimum/maximum dimension increases by rounding up the non-compliance to the next complete unit
of measure (1.0mm or 1.0g). The penalty is applied once for every complete unit outside of the absolute
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 16 of 58 24 July 2025
minimum/maximum dimension. For example:
T2.6 Design ideas and regulation compliance questions
Teams are not permitted to seek a ruling from STEM Racing Limited or any competition officials or
judges before the event as to whether a design idea complies with these regulations, any regulatory
communication between teams and ICCs or teachers is only for guidance, rulings will only be made by
the official judges at the World Finals event. Design compliance to the regulations forms part of the
competition. As in Formula 1® innovation is encouraged and STEM Racing™ teams may also find ways
of creating design features that push the boundaries of the regulations in order to get an extra
competitive edge.
T2.7 Measurements
T2.7.1 All dimensions and weights are presented as absolute minimum or maximum, unless stated
otherwise. For example:


T2.7.2 Dimensional measures - all car component dimensions or weight are inclusive of any applied
paint finish or decal. A series of specially manufactured gauges will be used to broadly verify
dimensional compliance. Accurate measuring tools, such as vernier callipers, will then be used to
closely inspect any dimensions found to be close to the dimensional limits per the initial gauge
inspection. IMPORTANT: Some regulations are assessed with a full 8g race cartridge fully inserted into
the cartridge chamber. For compliance with these regulations, the static weight distribution of the car
must be such that the car is capable of resting on all four (4) wheels without any outside assistance.
T2.7.3 Weight measures – all weight measurements will be made using the STEM Racing Limited
calibrated electronic competition scales.
T2.8 Benefit of doubt
The chair of judges will, where appropriate, seek to use ‘benefit of doubt’ when the assessment of
compliance is marginal or unclear. In this situation, teams will be given the benefit of doubt rather than a
firm penalty if a penalty cannot be clearly measured or identified.
MIN Weight
Absolute Min: 48.0g
MIN Dimension
Absolute Min: 26.0mm
MAX Dimension
Absolute Max: 34.0mm
48.0g - PASS 26.0mm - PASS 34.0mm - PASS
47.9g - FAIL 25.9mm - FAIL 34.1mm - FAIL
T9.5.1 Rear wing span: [PERFORMANCE | Penalty - 2pts per millimetre]
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 17 of 58 24 July 2025
T2.9 Spirit of the competition
Teams are expected to act in the spirit of the competition, both before and during the STEM Racing™
World Finals. Any team or individual team member deemed by the chair of judges to be acting outside
of the spirit of the competition, can be removed from certain or all aspects of the competition. For
example, a team or individual team member attempting to abuse the technical regulations to their
advantage may, at the discretion of the chair of judges, be removed from racing and receive no points
for this activity. A team or individual team member deemed to be acting in an unsportsmanlike manner
towards another team or other persons may be removed from some or all judging areas.
The spirit of the competition is simple; embrace and respect the rules and regulations, do your very best
to compete legally and fairly, while contributing positively to the STEM Racing™ World Finals. Make
friends, create positive relationships, network professionally and enjoy yourselves.
T2.10 Originality of Work
STEM Racing Limited welcomes and endorses innovation and does not consider that plagiarism should
play any part in any of the disciplines that make up the competition.
Competing teams at all levels of the competition that intentionally plagiarise any part of their assessed
work, undermines the credibility and integrity of the STEM Racing™ challenge and the spirit of the
competition. At the Aramco STEM Racing™ World Finals 2025, STEM Racing™ shall be implementing
various originality detection methodologies and requesting all competing teams to submit an originality
declaration.
Further details and associated penalties will be explained in detail in the Aramco STEM Racing™
World Finals 2025 competition regulations.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 18 of 58 24 July 2025
Article T3: Fully assembled car 19
Article T4: Car body 22
Article T5: Power unit cartridge chamber 25
Article T6: Tether line guides 28
Article T7: Wheels 30
Article T8: Nose, Front Wings/support 35
Article T9: Rear Wings/support 41
Article T10: Additional Components 45
COMPLIANCE AND PENALTIES
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 19 of 58 24 July 2025
ARTICLE T3 – FULLY ASSEMBLED CAR
T3.1 Design and manufacture – [GENERAL | Penalty – 5pts each]
T3.1.1 All STEM Racing™ cars must be designed and engineered using CAD (Computer Aided
Design) and CAM (Computer Aided Manufacture) technology. CAD software used should provide for 3D
part modelling, assembly and 3D realistic rendering. We recommend the use of Autodesk Fusion 360
software. The CAM package should allow students to simulate CNC machining processes so they can
show evidence of these in their portfolio. We recommend the use of Denford QuickCAM PRO software.
T3.1.2 The body of all STEM Racing™ cars must be manufactured via material removal using a CNC
router/milling machine. We recommend all teams use a Denford CNC Router. This manufacturing
process should occur at your school/college or at a designated manufacturing centre/partner site.
T3.1.3 An official STEM Racing™ holographic sticker from the official STEM Racing™ Model Block for
each car must be submitted on the project element submission sheet at the World Finals event
registration. F1 in Schools stickers will also be permitted for 2025 only.
T3.1.4 The individual components of both race cars must be designed with identical geometry.
T3.2 Safe Construction [SAFETY | Penalty – 10pts each]
T3.2.1 Specification judging - all submitted cars will be inspected closely to ensure that they are
engineered and constructed safely for the purpose of racing. If the judges rule an aspect of either race
car to be unsafe for racing, the team will be required to carry out repairs / modifications to the car(s).
Any such repair work will result in a penalty of 10 points per unsafe car.
T3.2.2 During racing – the race officials will routinely inspect cars for safety during scheduled races. If
the officials rule a car to be unsafe, a penalty of 10 points will be imposed at the discretion of the Chair
of Judges. The team may repair the car as per the Competition Regulations – C10 Car Repairs and
Servicing.
T3.3 Defined features – [PERFORMANCE | Penalty – 20pts]
The car assembly must only consist of components listed in ARTICLE T1.1.
T3.4 Total width – [GENERAL | Penalty – 5pts per millimetre]
Total width is the maximum assembled car width, measured normal to the vertical reference plane,
between the outer edges of the widest feature of the car assembly.
Absolute Min: 65.0mm / Absolute Max: 85.0mm
T3.5 Total height – [GENERAL | Penalty – 5pts per millimetre]
Total height is the maximum assembled car height, normal to the vertical reference plane, between the
track surface and the highest feature of the car assembly. This is measured with a full 8g power unit
cartridge inserted into the cartridge chamber with the car sitting on all four (4) wheels with no outside
assistance.
Absolute Max. 65.0mm
Total height Max 65.0mm
Total widht Max 85.0mm
Total Width Min 65.0mm Max 85.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 20 of 58 24 July 2025
T3.6 Total weight – [PERFORMANCE | Penalty – 10pts per gram]
Total weight is the weight of the car excluding a power unit cartridge. If ruled underweight at car
registration and confirmed during initial specification judging using the official competition scales, the
above points penalty will be applied. No car will race underweight and ballast will be added to the
underside of the car at 0.2g for every 0.1g underweight.
Absolute Min: 48.0g
T3.7 Track clearance – [GENERAL | Penalty – 10pts per millimetre]
Track clearance is the distance between track surface and any car component as listed in T1.1, except
wheels. Measured normal to the track surface. This is measured with a full 8g power unit cartridge
inserted into the cartridge chamber with the car sitting on all four (4) wheels with no outside assistance.
Absolute Min: 1.5mm
Track clearance Min 1.5mm
T3.8 Status during racing - [GENERAL | Penalty – 5pts]
The car assembly must be designed so that no items other than those listed in T3.9, or power unit
cartridges are removed, replaced or added to the assembly during scheduled race events.
T3.9 Replacement Components [GENERAL]
Any spare / replacement components should be identical in design and geometry to those fitted to the
car and must be submitted with the cars at registration. Only the following spare / replacement
components are permitted:
Component Max Quantity
Nose cone & front wing assembly 2
Rear wing assembly 2
Front wheels 4
Front wheel support structure 2
Rear wheels 4
Rear wheel support structure 2
Front tether line guide 2
Rear tether line guide 2
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 21 of 58 24 July 2025

T3.9.1 Submitted components – [GENERAL]
Only submitted replacement components that are determined by the judges to be identical in design
and geometry to those fitted to the cars will be allowed to be used during track repairs or post-race
servicing.

T3.9.2 Introduced components - [GENERAL | Penalty – 5pts per component]
If any other items need to be introduced for car repairs a 5pt penalty will be incurred per component
item.
Rear wheel
support
x 2
Front wheel
support
x 2
Front wheels
x 4
Rear wheels
x 4 Nose cone
assembly
x 2
Rear wing
assembly
x 2
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 22 of 58 24 July 2025
ARTICLE T4 – BODY
T4.1 Body construction – [GENERAL | Penalty – 20pts]
A single continuous piece of CNC manufactured STEM Racing™ Model Block material must exist rear
of the reference plane A, encompassing both the virtual cargo and power unit cartridge chamber.
T4.2 Virtual cargo – [PERFORMANCE | Penalty – 25pts]
A virtual cargo must be completely encompassed by the body and be wholly positioned between the
front and rear wheel centre lines. The virtual cargo must have minimum dimensions as shown below,
with its top surface located symmetrically about and positioned normal (90 degrees) to the vertical
reference plane. The virtual cargo may also share common faces with the car body. All dimensions
shown are absolute minimum. The Virtual Cargo can coincide with the legal ballast container but not the
halo pocket.
T4.3 Virtual cargo identification – [GENERAL | Penalty – 5 pts]
The virtual cargo location and compliance MUST be clearly dimensioned (such as from either the front
or rear axle centre lines and height above the track). The virtual cargo MUST be identified by hatching,
shading or block colour, or outlined with a contrasting colour line within the engineering drawings
submitted for scrutineering. Please refer to the example diagram below, showing the virtual cargo
clearly highlighted in red:
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 23 of 58 24 July 2025
T4.4 Halo
T4.4.1 Halo – [PERFORMANCE | Penalty – 10 pts]
The Halo (refer ARTICLE T1.21) MUST be included in the car design without any dimensional or
surface profile changes. The file (halo_2025_with_6mm_hole_and_sr_logo) can be downloaded from
https://www.stemracing.com/downloads.html Please see appendix ix for detailed dimensions.
T4.4.2 Halo visibility front and side views – [GENERAL | Penalty – 10 pts]
Visibility of the Halo must not be physically obstructed by any other component when viewed in the front
or side views.
SIDE VIEW
When viewed from the side, everything
inside the red outline MUST be visible.
FRONT VIEW
When viewed from the front,everything
inside the red outline MUST be visible.
T4.4.3 Halo visibility top view – [GENERAL | Penalty – 10 pts]
The Halo must not be physically obstructed in the plan view except by the helmet.

TOP VIEW
When viewed from the top, everything
inside the red outline MUST be visible.



Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 24 of 58 24 July 2025
T4.4.4 Halo circular notch height– [SAFETY | Penalty – 5pts]
To be effective the centre of the Circular Notch must be 34.0mm (±1.0mm) above the track surface. To
achieve this the bottom of the halo pocket must be 24.0mm and parallel to the track surface in the
assembled car.
T4.4.5 Halo Safety Test– [SAFETY | Penalty – 5pts]
With the car supported on a power unit cartridge a 1kg load will be suspended to give a loading of 2kg
(to be reviewed) at point of contact on the Halo circular notch.
T4.5 Helmet – [GENERAL | Penalty – 5pts]
The Helmet is a standard part designed by STEM Racing™ that MUST be included in the car design
without any dimensional changes. The Helmet is available to download as a universal 3D part from the
STEM Racing™ website. For this part (2025_helmet_with_6mm_dia_spigot_final) and more free
downloads, please visit https://www.stemracing.com/downloads.html
The helmet may be manufactured out of any material.
We suggest that the helmet be painted in the team’s country or hero driver colours

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 25 of 58 24 July 2025
T4.6 STEM Racing™ logo decal location – [GENERAL | Penalty – 5pts]
A STEM Racing™ logo decal (refer ARTICLE T1.12) must be wholly adhered to each side of the car,
and be 100% visible in the respective side view. Teams may manufacture their own decals but must
use the artwork supplied by STEM Racing.
T4.7 Team Number – [GENERAL | Penalty – 2pts]
After registering for the World Finals event each team shall be issued with their official team number.
This must be displayed on the car body between the front edge of the halo and reference plane A. The
number should be clearly visible in the plan view and a minimum text height of 8mm. If a team submits
their car without the team number, then one will be provided at the World Finals event.
Additionally, teams must also display “A” or “B” on the respective cars with a minimum text height of
8mm, as demonstrated below.
Teams may additionally include the team number elsewhere on the car such as the rear wing
endplates.
Minimum text height: 8.0mm

T4.8 Decal thickness – [GENERAL | Penalty – 5pts]
This is measured as the total thickness of any decal, excluding any surface finishes.
Absolute Max: 0.5mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 26 of 58 24 July 2025
ARTICLE 5 – POWER UNIT CARTRIDGE CHAMBER
T5.1 Diameter – [SAFETY | Penalty – 5pts]
This is the diameter of the power unit cartridge chamber, measured at any point through its minimum
depth.
Absolute Min: 18.0mm / Absolute Max: 18.5mm
T5.2 Distance from track surface – [GENERAL | Penalty – 5pts per millimetre]
This is measured with a full 8g power unit cartridge inserted into the cartridge chamber, from the rear
centre of the power unit cartridge to the track surface, measured normal to the track surface with the car
sitting on all four (4) wheels with no outside assistance.
Absolute Min: 30.0mm / Absolute Max: 40.0mm
T5.3 Depth – [SAFETY | Penalty – 5pts]
The depth of the chamber is measured parallel to the vertical reference plane anywhere around the
chamber circumference from the opening to the chamber end.
Absolute Min: 45.0mm / Absolute Max: 58.0mm
T5.4 Max angle of chamber – [SAFETY | Penalty – 5pts]
The absolute maximum angle of the chamber, parallel to the track surface. This is measured with a full
8g power unit cartridge inserted into the cartridge chamber with the car sitting on all four (4) wheels with
no outside assistance.
Absolute Min: -3° Absolute Max: 3°
T5.5 Chamber safety zone – [SAFETY | Penalty – 10pts]
A safety zone of STEM Racing™ Model Block material with a minimum thickness of 3.0mm must be
maintained around the minimum chamber depth (see T5.3). The chamber safety zone and connection
to the car body will be assessed and if determined below the minimum thickness, may be considered a
safety issue at the judge’s discretion, see ARTICLE T3.2.
IMPORTANT: the entire circumference and depth of the power unit cartridge chamber must not be
intersected by any object.
Absolute Min: 3.0mm
(The cartridge chamber should be free of any paint)

3.0mm Safety zone
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 27 of 58 24 July 2025
T5.6 Power unit cartridge visibility – [PERFORMANCE | Penalty – 10pts per
millimetre]
When fully inserted, the power unit cartridge must extend at least 5.0 mm beyond the rear of the car. It
must be completely visible from all angles around the longitudinal centerline of the cartridge (i.e., when
viewed in a full 360° sweep around its axis).
Absolute Min: 5.0mm
 5.0mm
Power unit cartridge
T5.6: Minimum protrusion in top, bottom and side view
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 28 of 58 24 July 2025
ARTICLE T6 – TETHER LINE GUIDES
T6.1 Location – [SAFETY | Penalty – 10pts]
Each car must have only two (2) firmly secured tether line guides, one on or up to 10.0mm in front of the
front axle centre line and one on or up to 10.0mm behind the rear axle centre line of the car. The track
tether line must only pass through the two tether line guides during racing.
T6.2 Internal dimension – [SAFETY | Penalty – 5pts]
This is the minimum and maximum internal measurement of the opening within the guide, which the
tether line passes through. This will be measured using a 3.5mm and/or 6.0mm diameter tool.
Absolute Min: 3.5mm / Absolute Max: 6.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 29 of 58 24 July 2025
T6.3 Tether line guide safety – [SAFETY | Penalty – 10pts]
The guide holes must be completely closed to prevent the tether line from slipping out during racing.
The construction of the tether line guides will be closely examined in relation to safety, please refer to
ARTICLE T3.2 for more information. The guides must be robust so as to prevent the diameter or shape
changing during racing. The below tether line guide test will be conducted during scrutineering. A 200g
weight will be suspended from each tether line guide to check the guides are securely fitted to the car
and safe to race.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 30 of 58 24 July 2025
ARTICLE T7 – WHEELS AND WHEEL SUPPORT
STRUCTURES
T7.1 Number and location – [GENERAL | Penalty – 25pts]
The car assembly must include four (4) cylindrical wheels, a maximum of two (2) at the front and a
maximum of two (2) at the rear. Opposing wheels must share a common centre line / axis.
T7.2 Distance between opposing wheels – [PERFORMANCE | Penalty – 2.5pts per
millimetre per axle]
This is measured as the innermost distance of the rotating wheel components (other than a rotating
axle) between the two (2) opposing wheels measured parallel to the track surface.
T7.2.1 Front Axle - Absolute Min: 38.0 mm
T7.2.2 Rear Axle - Absolute Min: 30.0 mm
T7.3 Wheelbase – [PERFORMANCE | Penalty –5pts per millimetre]
The wheelbase of the vehicle is the distance between the centre line of the front and rear wheels as
viewed in the side view.
Absolute Min: 120.0mm / Absolute Max: 140.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 31 of 58 24 July 2025
T7.4 Track contact width – [PERFORMANCE | Penalty – 2.5pts per millimetre per
wheel]
This is measured along the surface of the wheel that makes constant contact with the track surface,
excluding any chamfers or fillets.
If only one wheel per axle is outside of the minimum or maximum dimension, the point penalty will stand
but the regulation is reclassified as General.
T7.4.1 Front wheels - Absolute Min: 13.0mm
T7.4.2 Rear wheels - Absolute Min: 17.0mm
T7.5 Diameter – [PERFORMANCE | Penalty – 2.5pts per millimetre per wheel]
This is the wheel diameter measured across the minimum track contact width rolling surface.
If only one wheel per axle is outside of the minimum or maximum dimension, the point penalty will stand
but the regulation is reclassified as General.
Absolute Min: 28.0mm / Absolute Max: 32.0mm
T7.6 Race track contact – [PERFORMANCE | Penalty – 2.5pts per wheel]
All four (4) wheels must touch the racing surface at the same time across the full track contact width,
measured with a full power unit cartridge inserted with the car sitting on all four (4) wheels with no
outside assistance. Race track contact must be maintained prior to car launch and during racing.
T7.7 Rolling surface – [PERFORMANCE | Penalty – 2.5pts per wheel]
The wheel diameter must be consistent across the track contact width. (i.e. no tread like features are
permitted)
T7.8 Rotation – [PERFORMANCE | Penalty – 5pts per wheel]
To facilitate forward motion of the car during racing all (4) wheels must rotate freely about their axis
using a 3° maximum inclined surface.
Absolute Max: 3°

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 32 of 58 24 July 2025
T7.9 Visibility in top and bottom views – [PERFORMANCE]
The visibility of all wheels must not be physically obscured by any component of the car in the car’s top
and bottom elevation views. Car body or any other components must not exist within the dimensions
illustrated below. These dimensions must exist from the inside edges of each wheels’ track contact
width to the extreme width of the car assembly and a height from track surface of 65.0mm. This is
measured, parallel to the vertical reference plane and track surface. Please also refer to T8.6 and T9.6
– Clear Airflow.
Regulation Location Dimension Penalty
T7.9.1 In front of front
wheels Absolute Min: 5.0mm 2.5pts
T7.9.2 Behind front wheels
Absolute minimum dimensions on diagram
below
5pts
T7.9.3 In front of rear
wheels
Absolute minimum dimensions on diagram
below
5pts
T7.9.4 Behind rear wheels Absolute Min: 5.0mm 2.5pts
Scrutineering tools used to define these clearances will be manufactured to dimensions as illustrated
below.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 33 of 58 24 July 2025
T7.10 Visibility in side views – [PERFORMANCE | Penalty – 10pts per wheel]
The visibility of all wheels must not be physically obscured by any component of the car with the
exception of any wheel support systems, in the car’s side elevation views.
T7.11 Visibility in front view – [PERFORMANCE | Penalty – 10pts per millimetre]
The visibility of the front wheels in the car’s front view may only be physically obstructed to a height of
20.0mm from the track surface. This is measured with a full 8g power unit cartridge inserted into the
cartridge chamber with the car sitting on all four (4) wheels with no outside assistance.
Absolute Max: 20mm
T7.12 Wheel support – [GENERAL | Penalty – 5pts each]
T7.12.1 Wheel support systems: Wheel support systems may only exist within the cylindrical volume
generated through the diameter of the two (2) opposing wheels. Refer to ARTICLE T3.8 Track
clearance.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 34 of 58 24 July 2025
T7.12.2 Wheel support systems identification: The surfaces defining the wheel support structures
MUST be dimensioned and identified clearly by hatching, shading or block colour within the engineering
drawings submitted for scrutineering. (Construction lines are acceptable to define the boundaries
between components such as nose cone and wing support structures.) Also refer to the definition in
ARTICLE T1.15 for guidance on annotating these features in your Engineering Drawings.
T7.13 Wheel safety test [SAFETY | Penalty – 2.5pts per wheel]
To prevent wheel detachment during racing and encourage good engineering practice a wheel safety
test will be carried out.
The wheels must be robust so as to prevent the diameter or shape changing during racing. The below
wheel test will be conducted during scrutineering. A 100g weight will be suspended from each wheel.
To allow for this wheel safety test a minimum clearance (see below) is required from the inner corner of
the wheel to the car body.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 35 of 58 24 July 2025
ARTICLE T8 – NOSE, FRONT WING, END PLATES AND WING
SUPPORT STRUCTURES
T8.1 Nose, front wing, end plates and wing support structure identification –
[GENERAL | Penalty – 5pts]
The surfaces defining the nose, front wing(s), end plates and wing support structures must be
dimensioned and identified clearly by hatching, shading or block colour within the engineering drawings
submitted for scrutineering. (Clearly labelled construction lines are acceptable to define the boundaries
between components such as nose cone and wing support structure). Also refer to the definition in
ARTICLE T1.15 for guidance on annotating these features in your Engineering Drawings.
T8.2 Nose cone assembly dimension - [GENERAL | Penalty – 5pts each]
This is measured in front of and parallel to reference plane A to the extreme front of the fully
assembled car. From the Reference plane A the nose cone overhang is 40mm maximum.
Absolute Max: 40.0mm
T8.3 Front wing(s) description and placement – [General | Penalty – 5pts]
The design of the car should resemble an actual F1® car through the inclusion of a wing(s) on the nose
of the car. Each wing section must have a leading edge and a trailing edge across its full span. Refer to
the definition in ARTICLE T1.5.
T8.4 Front wing(s) construction and rigidity – [General | Penalty – 5pts]
The nose, front wing(s) and any support structures may be manufactured from any separate materials.
The wing span dimension must remain unchanged during races (i.e. wings must be rigid, ruled at the
judge’s discretion).

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 36 of 58 24 July 2025
T8.5 Nose, front wing(s), front wing end plates and wing support location
 T8.5.1 Nose and wing support structure location - [General | Penalty – 10pts]
The nose and front wing support structure must be in front of reference plane A, no more than 25.0mm
above the track surface and no wider than 15mm either side of the centre line reference plane.
Absolute Max height: 25.0mm

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 37 of 58 24 July 2025
T8.5.2 The front wing and front wing end plate location - [General | Penalty – 10pts]
The front wing and front wing end plates must be in front of reference plane A. The front wing must be
no more than 20.0mm above the track surface when wider than 15mm either side of the centre line.
Absolute Max height: 20.0mm
T8.5.3 Front wing end plate location - [General | Penalty – 10pts]
The front wing endplates must be positioned outside the minimum legal span, with a maximum width of
10.0mm when measured perpendicular to the vertical reference plane, and must not extend more than
25.0mm above the track surface when positioned outside (beyond) the front wheels.
Absolute Max Width: 10.0mm / Absolute Max Height: 25.0mm
The endplates may also play a role in breaking the beam that detects cars crossing the finish line. To
maximize accuracy in timing and classification, they should be designed to ensure they reliably trigger
the beam as early as possible. Considerations should include their height, width, and position relative to
the beam to optimize detection.
Please see Appendix i: Start Box and Finish Gate for beam information.

Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 38 of 58 24 July 2025
T8.6 Front Wing Dimensions – [PERFORMANCE]
 T8.6.1 Front wing span - [PERFORMANCE | Penalty – 2pts per millimetre]
The front wing span will be measured at right angles to the vertical reference plane along the leading
edge, trailing edge, top surface and bottom surface of the wing, whichever is shortest will be considered
as the maximum span. Where the front wing span is intersected by another part of the car, the total
span is the sum of a maximum of two (2) wing segments, which must be no less than 25.0mm each.
(See illustration below)
Absolute Min: 25.0mm x 2 = 50.0mm or 50.0mm x 1 = 50.0mm


Single Vane
Multi Vane
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 39 of 58 24 July 2025
T8.6.2 Front wing chord - [PERFORMANCE | Penalty – 1pt per millimetre]
The front wing chord minimum to maximum dimensions must exist throughout the existing wing span.
The chord is the distance between the leading edge and trailing edge of up to three elements that must
overlap, it will be measured parallel to the vertical reference plane and normal to the track surface.
Front wing chord compliancy does not depend on span. Multi vane wings must overlap. (See illustration
below and appendix v)
Absolute Min: 15.0mm / Absolute Max: 25.0mm
T8.6.3 Front wing thickness - [PERFORMANCE | Penalty – 1pt per millimetre]
The wing thickness minimum to maximum dimensions must exist throughout the wing’s existing span
and at a point along the existing chord. Front wing thickness compliancy does not depend on span and /
or chord. (See illustration below)
Absolute Min: 2.0mm / Absolute Max: 6.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 40 of 58 24 July 2025
T8.7 Front wing clear airflow - [PERFORMANCE | Penalty – 5pts]
The front wing(s), measured across its / their minimum existing span, must have a minimum of 5.0mm
of clear ‘air’ space to any other part of the car or track surface, measured normal from any part of the
wings surface.
Absolute Min: 5.0mm
(To allow for fillet rads where a wing joins a support structure this will be checked with a 5.0mm
diameter spherical ball on the end of a 2mm diameter rod.)
SINGLE VANE MULTI VANE
T8.8 Front wing visibility – [PERFORMANCE | Penalty – 10pts]
Visibility of the front wing(s) must not be physically obstructed by any other component when viewed in
the front view.

5.0mm diameter spherical ball 2mm diameter rod
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 41 of 58 24 July 2025
ARTICLE T9 – Rear wing and wing support structures.
T9.1 Rear wing and wing support structure identification – [General | Penalty – 5pts]
The surfaces defining the rear wing and wing support structure(s) must be dimensioned and identified
clearly by hatching, shading or block colour within the engineering drawings submitted for scrutineering.
(Clearly labeled construction lines are acceptable to define the boundaries between components such
as car body and wheel support structures). Also refer to the definition in ARTICLE T1.15 for guidance
on annotating these features in your Engineering Drawings.
T9.2 Rear wing description and placement – [General | Penalty – 5pts]
The design of an STEM Racing™ car should resemble an actual F1® car through the inclusion of a wing
at the rear of the car. To be considered a wing section it must have a leading edge and a trailing edge
across its required span. Refer to the definition in ARTICLE T1.5
T9.3 Rear wing construction and rigidity – [General | Penalty – 5pts]
The rear wing and any support structures may be manufactured from any separate materials. The wing
span dimension must remain unchanged during races (i.e. wings must be rigid, ruled at the judge’s
discretion).
T9.4 Rear wing, wing support structure and rear overhang location
T9.4.1 Rear wing and wing support structure location [General | Penalty – 10pts]
The whole of the rear wing and any support structure must be to the rear of reference plane B.
T9.4.2 Rear overhang length [General | Penalty – 5 pts] This is measured to the rear of and parallel
to reference plane B to the extreme rear of the fully assembled car. From the Reference plane B the
rear wing and wing support structure overhang is a maximum of 40.0mm.
Absolute Max: 40.0mm
T9.4.3 Rear overhang height [General | Penalty – 5 pts] This is measured to the rear of reference
plane B to the highest point of the fully assembled car from the track surface.
Absolute Max: 65.0mm
 Overhang height Max: 65.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 42 of 58 24 July 2025
T9.5 Rear wing dimensions – [PERFORMANCE]

T9.5.1 Rear wing span - [PERFORMANCE | Penalty - 2pts per millimetre]
The rear wing span will be measured at right angles to the vertical reference plane along the leading
edge, trailing edge, top surface or bottom surface of the wing, whichever is shortest will be considered
as the maximum span. The rear wing must exist as a single, unbroken minimum span of 50.0mm.
(See illustration below)
Absolute Min: 50.0mm
T9.5.2 Rear wing chord - [PERFORMANCE | Penalty - 1pt per millimetre]
The rear wing chord minimum to maximum dimensions must exist throughout its existing wing span.
The chord is the distance between the leading edge and trailing edge of up to two elements that must
overlap, it will be measured parallel to the vertical reference plane and normal to the track surface. Rear
wing chord compliancy does not depend on span. Multi vane wings must overlap. (See illustration below
and appendix v)
Absolute Min: 15.0mm / Absolute Max: 25.0mm

Single Vane Multi Vane
Chord Min 15.0mm
Chord Min 15.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 43 of 58 24 July 2025
T9.5.3 Rear wing thickness - [PERFORMANCE | Penalty - 1pt per millimetre]
The wing thickness minimum to maximum dimensions must exist throughout the wing’s existing span
and at a point along the existing chord. Rear wing thickness compliancy does not depend on span and /
or chord. (See illustration below)
Absolute Min: 2.0mm / Absolute Max: 6.0mm









T9.5.4 Rear wing height deviation - [GENERAL | Penalty - 1pt per millimetre]
The maximum change in height deviation from the highest point of the wing is 15mm. Measured along
the minimum span on the top surface.
Absolute maximum height deviation: 15.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 44 of 58 24 July 2025
T9.6 Rear wing clear airflow – [PERFORMANCE | Penalty – 5pts]
The rear wing, measured across its existing span, must have a minimum of 5.0mm of clear ‘air’ space to
any other part of the car or track surface, measured normal from any part of the wings surface.
Absolute Min: 5.0mm
(This will be checked with a 5.0mm diameter spherical ball on the end of a 2mm diameter rod.)
5.0mm diameter spherical ball 2mm diameter rod
5.0mm Clear
airflow
5.0mm Clear
airflow
5.0mm Clear
airflow
5.0mm Clear
airflow
Multi vane Single vane
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 45 of 58 24 July 2025
T9.7 Rear wing visibility – [PERFORMANCE | Penalty – 10pts]
Visibility of the rear wing must not be physically obstructed by any other component when viewed in the
front view
Illustrations for T8 and T9 below:
(See Appendix iii for more detail, examples and penalties relating to wing span, chord and thickness)


ARTICLE T10 – Additional Components
T10.1 Description and placement [GENERAL]
Only the power unit cartridge, as positioned by race officials, is permitted to make contact with the
launch pods and/or cars prior to and/or during racing. Please refer also to the Aramco STEM Racing™
World Finals 2025 Competition Regulations.
Visibility of rear wing not
physically obstructed in front
view
(Illustrated here as
1 x 50mm single span) (Illustrated here as
2 x 25mm span segments)
T9.5.1 Rear wing span T8.5.1 Front wing span
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 46 of 58 24 July 2025
Appendix i: Start Box / Finish Gate 47
Appendix ii: Official STEM Racing®
 Model Block dimensions 48
Appendix iii: Front wing compliance examples 49
Appendix iv: Rear wing compliance examples 51
Appendix v: Wing overlap 53
Appendix vi: Official Power Pack dimensions 54
Appendix vii: Car Deceleration System 54
Appendix viii: Component identification example 55
Appendix ix: Halo & Ballast 56
APPENDIX
OTHER INFORMATION & ILLUSTRATIONS
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 47 of 58 24 July 2025
APPENDIX – OTHER INFORMATION & ILLUSTRATIONS
i. Start Box and Finish Gate
The start boxes are designed to sit centrally within each lane of the track.
The distance from the emitter centre line to the race track surface on both lanes is ~7mm.

Light beam
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 48 of 58 24 July 2025
ii. Official STEM Racing™ Model Block Dimensions
Below: orthographic projection of STEM RACING™ Model Block. All dimensions shown in millimetres
This component is available to download as a universal 3D part from the STEM Racing™ website. For
this part and more free downloads, please visit
https://www.stemracing.com/downloads.html
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 49 of 58 24 July 2025
iii. Front wing compliance examples
The following table shows how penalty points are awarded for front wing span, chord or thickness
dimensions that do not meet the specifications set out in T8.5.1, T8.5.2 and T8.5.3.
This is not an exhaustive list of all possible wing configurations.
Front Wing Examples – Single Vane
T8.5.1
Span
-2pts per mm
T8.5.2
Chord
-1pts per mm
T8.5.3
Thickness
-1pts per mm
Remarks
PASS PASS PASS
Wing span is split by single
mounted central wing
support.
Wing span segments are
minimum length, therefore
PASS
Wing chord is minimum
throughout the existing span,
therefore PASS.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore
PASS.
FAIL PASS PASS
Wing span is split by nose.
Wing span segments are less
than minimum length at trailing
edge (rear of wing), therefore
FAIL
Wing chord is minimum
throughout the existing span,
therefore PASS.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore
PASS.
PASS PASS FAIL
Wing span is split by nose.
Wing span segments are
minimum length, therefore
PASS
Wing chord is minimum
throughout the existing span,
therefore PASS.
Wing thickness is less than
minimum, therefore FAIL.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 50 of 58 24 July 2025
Front Wing Examples – Multiple Vanes
T8.5.1
Span
-2pts per mm
T8.5.2
Chord
-1pts per mm
T8.5.3
Thickness
-1pts per mm
Remarks
PASS FAIL PASS
Wing span is split by single
mounted central wing
support.
Wing span segments are
minimum length
(25mm+25mm), therefore
PASS
Wing chord is minimum
throughout the existing span,
but Multi vane wings do not
overlap FAIL.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore
PASS.
FAIL PASS PASS
Wing span is split by single
mounted central wing
support.
Wing span segments are less
than minimum length at trailing
edge (rear of wing), therefore
FAIL
Wing chord is minimum
throughout the existing span,
therefore PASS.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore
PASS.
PASS PASS FAIL
Wing span is split by single
mounted central wing
support.
Wing span segments are
minimum length
(25mm+25mm), therefore
PASS
Wing chord is minimum
throughout the existing span,
therefore PASS.
Wing thickness is over the
maximum limit, therefore FAIL.


Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 51 of 58 24 July 2025
iv. Rear wing compliance examples
The following table shows how penalty points are awarded for rear wing span, chord or thickness
dimensions that do not meet the specifications set out in T9.5.1, T9.5.2, T9.5.3, T9.5.4:
This is not an exhaustive list of all possible wing configurations.
Rear Wing Examples – Single Vane
T9.5.1
Span
-2pts
per
mm
T9.5.2
Chord
-1pt
per
mm
T9.5.3
Thickness
-1pt per
mm
T9.5.4
Deviation
-1pt per
mm
Remarks
PASS PASS PASS PASS
Wing span is minimum length,
therefore PASS.
Wing chord is minimum throughout the
existing span, therefore PASS.
Wing thickness is minimum throughout
the wing’s existing span and at a point
along the existing chord, therefore
PASS.
Rear wing deviation is below
maximum, therefore PASS.
PASS PASS FAIL PASS
Wing span is minimum length,
therefore PASS.
Wing chord is minimum throughout the
existing span, therefore PASS.
Wing thickness is more than maximum,
therefore FAIL.
Rear wing deviation is below
maximum, therefore PASS.
PASS FAIL PASS FAIL
Wing span is minimum length,
therefore PASS.
Wing chord is less than minimum
length, therefore FAIL.
Wing thickness is minimum throughout
the wing’s existing span and at a point
along the existing chord, therefore
PASS.
Wing deviation exceeds maximum
height, therefore FAIL.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 52 of 58 24 July 2025
Rear Wing Examples – Multiple Vane
T9.5.1
Span
-2pts
per mm
T9.5.2
Chord
-1pt per
mm
T9.5.3
Thickness
-1pt per
mm
T9.5.4
Deviation
-1pt per
mm
Remarks
PASS PASS PASS PASS
Wing span is minimum length,
therefore PASS.
Wing chord is minimum
throughout the existing span,
therefore PASS.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore PASS.
Wing deviation is minimum
throughout the existing span,
therefore PASS.
PASS FAIL PASS PASS
Wing span is minimum length,
therefore PASS.
Wing chord is minimum
throughout the existing span, but
Multi vane wings do not overlap
FAIL.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore PASS.
Wing deviation is minimum
throughout the existing span,
therefore PASS.
PASS FAIL PASS FAIL
Wing span is minimum length,
therefore PASS.
Wing chord is less than
minimum length, therefore FAIL.
Wing thickness is minimum
throughout the wing’s existing
span and at a point along the
existing chord, therefore PASS.
Wing deviation exceeds
maximum height, therefore
FAIL.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 53 of 58 24 July 2025
v. Wing Overlap
Wing overlap explanation:
How to check if a gap exists between the elements:
 Perpendicular to the track
Chord 15.0 to 25.0mm
Chord = 10.0mm Chord = 13.0mm
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 54 of 58 24 July 2025
vi. Official Denford Race Power Pack dimensions
This component is available to download as a universal 3D part from the STEM Racing™ website. For
this part and more free downloads, please visit
https://www.stemracing.com/downloads.html
Full weight of RACE Power Pack: between: 28.9g and 29.4g
vii. Car Deceleration System
The Halo Deceleration System acts to bring cars to rest once crossing the finish line. STEM Racing™
will provide a Halo Deceleration System which is integrated into the final track section after the finish
line. This consists of an arresting cable which is aligned with the circular notch of the Halo.
Please note:
The official STEM Racing™ Halo deceleration system will be the only permitted stopping
system. Please refer to the Aramco STEM Racing™ World Finals 2025 Competition Regulations
for full details.
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 55 of 58 24 July 2025
 viii. Example of component identification
This is a basic example of component identification. Ensure that the regulation numbers align with the
2025 Technical Regulations. For detailed guidance on identifying your components, refer to T1.15.
Front / Rear Wings
Rear Wing Support
Front Wing end plate
Nose Cone
Wheel Support System
Halo
Helmet
Body
Wheels
Tether Guides
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 56 of 58 24 July 2025
ix. Halo and Ballast container drawings
To accommodate the 'Halo', your car will require a pocket cut (which will include a Ballast container
directly below the helmet aperture) the dimensions in the drawing below using a 6.35mm (1/4") or
smaller ball nose tool to a depth of 3.175mm.
The centre of the Halo 'Circular notch' for the retardation device is exactly 10.0 mm above the bottom of
the pocket. To be effective the centre of the Circular Notch must be 34.0mm ±1.0mm above the track
surface. To achieve this the bottom of the pocket must be 24.0mm above the track in the assembled
car. Use the dimensions on the diagrams below to check you have manufactured your Halo correctly
Legal Ballast
To help achieve the minimum weight, legal ballast may now be added to the legal ballast container
under the halo, accessible through the halo/helmet aperture. The Virtual Cargo can coincide/overlap
with the legal ballast container but not the halo pocket. The helmet should not be glued in place to allow
for ballast adjustments before scrutineering. Although the use of legal ballast is optional, if chosen, the
dimensions specified below are mandatory and must be strictly followed.
Halo and Helmet
above pocket and
legal ballast container
Halo pocket and legal
ballast container
dimensions
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 57 of 58 24 July 2025
Demonstration of compliance of Virtual Cargo and Legal Ballast Container
Please Remember:
The Virtual Cargo can coincide or overlap with the legal ballast container but not the halo pocket
Legal ballast Container
Virtual cargo
Isometric view of Halo
with 6.0mm hole
Example of Virtual Cargo
overlapping Legal Ballast
Container
Aramco STEM Racing World Finals 2025 - Technical Regulations – Revision 2
©2025 – STEM Racing Limited Page 58 of 58 24 July 2025
Please make sure you have also read the
Aramco STEM Racing™ World Finals 2025
Competition Regulations
For Official Technical & Competition Regulations Clarifications please email us at
global-admin@stemracing.com . All official clarifications will be posted on our official website.
Work hard,
see you at the
World Finals!
If you need any help at all, just get in touch with us:
STEM RACING™
+44 (0)20 7344 5390
global-admin@stemracing.com
www.stemracing.com
Í
2024/2025
REGULAMENTO
PROJETO SOCIAL
F1 in Schools™ - 2024/2025 Regulamento Projeto Social
Capa – Recoil Racing, Alemanha, Campeões Mundiais Aramco F1 in Schools 2023
CONTEÚDO
CLÁUSULA PS 1 – DEFINIÇÃO.............................................................................................................................3
PS 1.1 PORQUÊ DO PROJETO SOCIAL....................................................................................................3
 PS 1.2 O QUE SÃO PROJETOS SOCIAIS.............................................................................................................3
 CLÁUSULA PS 2 ELABORAÇÃO DO PROJETO SOCIAL...................................................................................3
 CLÁUSULA PS 3 CONTEÚDO DO PROJETO..................................................................................................5
 CLÁUSULA PS 4 ROTEIRO DO PROJETO SOCIAL - PORTFÓLIO.....................................................................5
PS 4.1 TERMO DE ABERTURA.............................................................................................................5
PS 4.2 PLANEJAMENTO......................................................................................................................5
PS 4.3 EXECUÇÃO...............................................................................................................................6
CLÁUSULA PS 5 FORMATO DA COMPETIÇÃO..............................................................................................6
PS 5.1 O QUE SERÁ JULGADO.............................................................................................................6
PS 5.2 PREPARAÇÃO DA EQUIPE.........................................................................................................6
PS 5.3 QUEM PRECISA PARTICIPAR....................................................................................................................6
PS 5.4 PROCESSO/PROCEDIMENTOS DE JULAGMENTO ................................................................................6
PS 5.5 REQUISITOS DO PORTFÓLIO DE PROJETO SOCIAL..............................................................................6
PS 5.6 PROJETO SOCIAL COMO CRITÉRIO DE DESEMPATE .............................................................................6
NOTAS – DIFERENÇA ENTRE AÇÃO SOCIAL E PROJETO SOCIAL.............................................................................7
APÊNDICE..........................................................................................................................................................7
 FICHA DE PONTUAÇÃO JULGAMENTO PROJETO SOCIAL ...........................................................................8
Favor observar: qualquer alteração feitas antes do evento será indicada usando texto vermelho sublinhado
F1 in Schools™ - 2024 Regulamento Projeto Social
©2024 - F1 in Schools Brazil 4 de 6 17 Julho 2024
CLÁUSULA PS1 – DEFINIÇÕES
PS 1.1 Porquê do Projeto Social
O projeto F1 in Schools busca proporcionar aos alunos participantes experiências
práticas de empreendedorismo, contato com novas tecnologias, explorar seus
potenciais e vivenciar o trabalho em equipe com todas as suas vertentes – liderança,
resiliência, abertura para o novo, saber ouvir, compartilhar, etc.
Com o propósito de trazer para o F1 in Schools também a preocupação de apresentar
aos alunos, escola e pais a importância da vivência do conceito de cidadania, o projeto
decidiu no Brasil pela obrigatoriedade de cada equipe em criar / participar de um ou
mais projetos sociais, atendendo a alguma demanda da comunidade ao entorno de
suas escolas.
PS 1.2 O que são Projetos Sociais
Projetos sociais são iniciativas individuais ou coletivas que visam proporcionar a
melhoria da qualidade de vida de pessoas e comunidades - organizando e
desenvolvendo projetos e ações sociais para transformar determinada realidade para o
bem comum sem fins lucrativos.
São ações estruturadas e intencionais que partem da reflexão e do diagnóstico sobre
determinada problemática, dentro dos limites de um orçamento e de um período de
tempo, buscando melhorar uma carência social.
Projeto Social não deve ser confundido com Ação Social. Enquanto que o primeiro visa
uma abrangência maior, iniciando com o entendimento do problema, planejamento de
sua execução, coordenação de participantes, verificação dos resultados alcançados e
garantia de continuidade do projeto, quer seja pela própria comunidade atendida e/ou
outros tais como por demais alunos da escola não participantes do F1 in Schools, suas
famílias e patrocinadores, a Ação Social refere-se mais a uma intervenção pontual tais
como arrecadação de roupas e/ou comida, recuperação de locais públicos (desde que
não envolva a comunidade na manutenção e gestão destes locais o que torna esta Ação
em um Projeto).
No caso de uma equipe aderir a um Projeto Social de ONG e/ou Instituição já existente,
será julgado como participação em projeto já existente.
Se uma equipe adotar o Projeto Social criado e desenvolvido anteriormente por alguma
equipe e apenas ampliar e/ou complementar o projeto, será julgado como participação
em projeto já existente.
CLÁUSULA PS2 – ELABORAÇÃO DO PROJETO SOCIAL
O ponto de partida é sempre uma realidade social, uma questão social:
Diagnóstico – Identificação do Problema:
F1 in Schools™ - 2024 Regulamento Projeto Social
©2024 - F1 in Schools Brazil 5 de 6 17 Julho 2024
 Solucionar um problema só é eficaz se parte de uma percepção acurada da
realidade. Para isso é necessário conhecer objetivamente o contexto onde irá
atuar e se tem condições de criar alternativas para reverter e/ou amenizar a
situação-problema.
 Fundamental a participação dos beneficiários em todas as etapas – serão coautores do projeto. (*)
 Identificar:
o Quem é o público alvo
o O que pensam
o Como vivem
o Quais os desejos e necessidades
 (*) Importante fazer esta pesquisa diretamente com os beneficiários – visitar o local e
o entorno da comunidade
 Pensar em como solucionar o problema ou carência e nas ações que poderiam
contribuir para mudar essa situação.
 As diferentes alternativas de solução imaginadas tem que ser analisadas para saber se
são viáveis.(**)
(**) Análise de Viabilidade: principais aspectos a serem considerados são: técnico,
operacional, social, financeiro e, às vezes, ambiental.
 Um objetivo deve ser:
o Verificável: a consecução do objetivo deve ser passível de comprovação:
o Alcançável: o objetivo deve indicar uma situação possível de ser concretizada;
o Realista: a avaliação das condições para realização do objetivo deve ser realista:
o Específico: o objetivo deve ser claro, bem definido e compreensível para
terceiros:
o Adaptado ao tempo: o objetivo deve poder ser alcançado no tempo previsto.
 Escolhida uma solução – qual a estratégia a ser aplicada - parte-se para programar
com detalhes o que vai ser feito, o que se espera que aconteça como resultado da
ação e o que se necessita agenciar e disponibilizar de modo a assegurar a realização
do projeto.
Sugestão: usar para a tarefa de planejamento das ações “Indicadores de Desempenho”:
eles servem para avaliar em que grau os objetivos e atividades de um projeto estão
sendo ou foram alcançados, dentro de certo tempo e em local definidos.
o Passos para a efetivação de um Projeto Social: Planejamento – Implementação –
Implantação – Controle – Avaliação
o Planejamento: fase do diagnóstico e a fase da elaboração do projeto em si.
o Implementação: significa tomar providências concretas para a realização de
F1 in Schools™ - 2024 Regulamento Projeto Social
©2024 - F1 in Schools Brazil 6 de 6 17 Julho 2024
algo planejado. Busca ou formalização e incorporação de recursos humanos,
físicos, financeiros, bem como a instrumentalização do planejamento.
o Implantação: aplicação das ações previstas para atingir o objetivo.
o Controle: monitoramento da execução
o Avaliação: mensuração do impacto produzido pelo Projeto Social
.
CLÁUSULA PS3 –CONTEÚDO DO PROJETO
 Título do Projeto: deve refletir o objetivo final do Projeto Social.
 Apresentação da Comunidade onde será aplicado.
 Justificativa: caracterizar a situação problema e a solução proposta.
 Objetivos e Metas:
o Objetivo Geral – resultados pretendidos.
o Objetivo Específico – decomposição do objetivo geral e metas concretas.
 Metodologia: atividades que serão implantadas/de que forma/apresentando metas
concretas. Cronograma.
 Controle e Avaliação:
o Controle - monitoramento da execução.
o Avaliação - mensuração do impacto produzido pelo Projeto Social.
CLÁUSULA PS4 –ROTEIRO DO PROJETO SOCIAL - PORTFÓLIO
PS 4.1 Termo de Abertura
 Identificação da Equipe (nome da equipe)
 Qual o escopo (Identificação da Equipe)
o Objetivo geral
o Objetivos específicos
o Quais as métricas escolhidas para monitorar o sucesso do projeto
 Resumo do projeto
 Em que realidade o projeto vai atuar (diagnóstico – o que o projeto vai solucionar)
 Qual o envolvimento da equipe no projeto
 Quais serão os parceiros do projeto e o tipo de contribuição
 Qual metodologia utilizada para execução do projeto
PS 4.2 Planejamento
 Qual o prazo total do projeto
 Quais os custos e as fontes de renda
 Quais os riscos envolvidos
 Como o projeto será divulgado
o Plano de comunicação interna
o Plano de comunicação externa
 Qual é a perspectiva/estratégia de continuidade do projeto após o término da parceria.
Descrever como se dará o processo de sustentação após a saída da equipe.
F1 in Schools™ - 2024 Regulamento Projeto Social
©2024 - F1 in Schools Brazil 7 de 6 17 Julho 2024
PS 4.3 Execução
 Evidências de monitoramento e controle do projeto
 Métricas – comparação dos resultados planejados x alcançados
 Lições aprendidas
 Depoimentos de pessoas atendidas pelo projeto social
CLÁUSULA PS 5 – FORMATO DA COMPETIÇÃO (até 80 pontos)
PS 5.1 O que será julgado?
Neste tópico serão julgadas a escolha do tema do Projeto Social bem como a sua
originalidade. Caso o projeto tenha sido criado pela equipe será analisada pela tabela
com a pontuação de até 80 pontos e, caso se trate de participação em um projeto já
existente ou continuidade de projeto anterior a equipe será analisada pela tabela com
pontuação até 70 pontos.
Outros pontos que serão avaliados são o grau de inovação/criatividadena escolha do
assunto, a relevância para a comunidade, o grau de envolvimento dos alunos, as ações
para garantir a perenidade do projeto - prever ações/mecanismos para que a
população-alvo e/ou outras pessoas possam dar continuidade ao projeto criado - e o
impacto do projeto na vida dos alunos.
PS 5.2 Preparação da equipe
As equipes podem mostrar materiais que estejam em seus estandes desde que
relacionados com o projeto social. Os juízes receberão antecipadamente uma cópia do
portfólio da equipe. Uso de computadores e/ou celulares é permitido para exibição de
fotos e vídeos.
PS 5.3 Quem precisa participar?
Todos os alunos devem participar e dar seus depoimentos individualmente
PS 52.4 Processo / procedimento do julgamento
Os juízes do Empreendedorismo Social avaliarão cada equipe durante cerca de 10 minutos
em ambientes determinados para tal. Os alunos responderão perguntas previamente
formuladas pelos juízes e terão abertura para fazerem seus comentários e perguntas.
PS 5.5 Requisitos do Portfólio e Vídeo do Projeto Social
As equipes devem elaborar um portfólio A4 (capa + 7 páginas) com fotos, depoimentos,
outras informações que julguem relevantes para comprovar e esclarecer a aplicação do
projeto.
Um vídeo de no máximo 2 minutos de duração deve ser elaborado contendo os alunos
explicando o propósito do projeto (1 minuto) e depoimentos de pessoas beneficiados
pelo projeto (1 minuto total). Os alunos devem obter uma autorização do uso de
imagem das pessoas entrevistadas.
PS 5.6 Projeto Social como critério de desempate
O tópico empreendedorismo Social existe apenas no Brasil pelo menos por enquanto.
A Organização Mundial incluiu na última edição da Final Mundial ocorrida em Abu
Dhabi 2019 a premiação referente ao Melhor Projeto de Sustentabilidade que não está
ligado a Projetos Sociais, mas sim com a preocupação com o tema Sustentabilidade na
execução do projeto F1 in Schools – materiais, meio ambiente, reaproveitamento,
F1 in Schools™ - 2024 Regulamento Projeto Social
©2024 - F1 in Schools Brazil 8 de 6 17 Julho 2024
práticas sustentáveis, etc.
O Projeto Social fará parte da pontuação geral das competições brasileiras. Assim, a
pontuação indicada na Final Mundial que é de no máximo 1.000 pontos, passará a ser
no máximo 1080 pontos nas competições realizadas no Brasil.
Nota: Diferença entre Ação Social e Projeto Social
 Uma determinada ONG tem como projeto social distribuir sopa para moradores de
rua. A equipe adere coletando alimentos, ajudando tanto na fabricação como
distribuição e/ou coletando materiais de higiene. Será considerada como ação social
dentro de um projeto já existente.
 Uma equipe criou um projeto para trazer renda para determinada comunidade. A
equipe atual adota este projeto e o complementa ensinando o uso de mídias sociais
para maior visibilidade da comunidade. Será considerada como ação social dentro de
um projeto já existente.
APÊNDICE…
1. Ficha de pontuação do empreendimento Social
Ficha de Pontuação de Projeto Social Número da Equipe:
Nome da Equipe:
País:
Projeto Criado
pelos Alunos
OU
Projeto novo, de
poucoimpacto
social, limitado
ao grupode
alunos
Projeto novo, que envolve
também outros projetos da
escola.
Projeto novo que não apresenta relação
com projetos anteriores e que extrapola
os muros da escola eatinge a comunidade
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
Participação em
Projeto Existente
Ação complementar a
um projeto já
existente.
Alunos participam ativamente de
um projeto já existente
Alunos ampliam um projeto já existente
envolvendo a comundade
1 2 3 4 5 6 7 8 9 1 0
Inovação /
Criatividade
Pouca pesquisa
sobre necessidade
efetiva
Alunos pesquisaram a
necessidade da escola e/ou
comunidade
A partir da pesquisa extensa baseada
em estudos da necessidade da
comunidade
1 2 3 4 5 6 7 8 9 1 0
Relevância Ação trouxe poucas
mudanças na comunidade
Ação realizada mudou a
realidade de apenas um
segmento
Ações trouxeram mudanças
significativas na comunidade
1 2 3 4 5 6 7 8 9 10 11 12 13
Envolvimento dos
Alunos
Parte do grupo
envolvido
Todo o grupo envolvido Além da equipe outros parceiros
atuaram ativamente na execução do
projeto social
1 2 3 4 5 6 7 8 9 10 11 12 13
Perenidade
O projeto não continua
após a saída dos
alunos
Alguns alunos continuam
envolvidos no projeto.
Alunos e novas pessoas continuam
envolvidos no projeto, sem prejuízo da
busca de novos projetos para a
temporada seguinte
1 2 3 4 5 6 7 8 9 1 0
Qualidade da
Documentação
Difícil de seguir com
padrão básico e
apresentação

 1 2 3
Estrutura clara, e bem
organizada.
4 5 6
Alto impacto e profissionalismo.
Organização consistente e clara
7 8
Transformação
em quem
participou
Alunos pouco afetados
Alunos mudaram a forma de
ser e avaliar o mundo após
o projeto
Alunos conseguiram trazer transformação
e mudanças para muitas pessoas
1 2 3 4 5 6 7 8
Avaliação Projeto Social Total =
Notas:
©2022- F1 in Schools™ Brazil 6 de 6 17 Abril 2022
In association with 1





PROJECT
MANAGEMENT
GUIDE 2023/24




In Association with

In association with 2
Table of Contents
STEM RACING & THE PROJECT MANAGEMENT EDUCATIONAL FOUNDATION................... 4
ABOUT PMIEF......................................................................................................................................................... 4
ABOUT THE PROJECT MANAGEMENT INSTITUTE.............................................................................. 4
PRINCIPLES OF PROJECT MANAGEMENT................................................................................................5
WHAT IS A PROJECT?......................................................................................................................................5
KEY ROLES IN PROJECT MANAGEMENT ..............................................................................................5
Project manager ................................................................................................................................................................5
Project stakeholder .........................................................................................................................................................5
Project sponsor .................................................................................................................................................................5
Project team members...................................................................................................................................................5
THE TRIPLE CONSTRAINTS OF PROJECT MANAGEMENT...........................................................6
THE PROJECT MANAGEMENT PROCESS ..................................................................................................7
OVERVIEW............................................................................................................................................................7
INITIATING PROCESS ...........................................................................................................................................8
DEFINING THE PROJECT................................................................................................................................8
IDENTIFY THE STAKEHOLDER ....................................................................................................................8
AUTHORISE THE PROJECT ...........................................................................................................................9
DELIVERABLES ...................................................................................................................................................9
MILESTONES .......................................................................................................................................................9
PLANNING PROCESS .........................................................................................................................................11
WRITING A SCOPE STATEMENT..............................................................................................................11
DEVELOPING THE WBS / PLANNING FOR QUALITY .......................................................................11
Sample Quality Acceptance Criteria.......................................................................................................................12
PLANNING WHEN AND HOW TO MONITOR AND CONTROL.................................................... 12
BUILDING A PROJECT SCHEDULE - per each deliverable of the WBS and the project ............................. 12
DETERMINE THE MAJOR CATEGORIES OF WORK: .........................................................................................12
DEFINE TASKS:.................................................................................................................................................................12
SAMPLE OF A WORK BREAKDOWN STRUCTURE............................................................................................13
DETERMINE THE SEQUENCE ....................................................................................................................................13
ESTIMATE TIME...............................................................................................................................................................13
BUILD THE SCHEDULE ..................................................................................................................................................13
SAMPLE SCHEDULE...................................................................................................................................................... 14
PLANNING FOR AQUIRING RESOURCES............................................................................................. 15
Sample Resource planning .........................................................................................................................................15
CREATING A BUDGET................................................................................................................................... 15
Sample Budget .................................................................................................................................................................16
PLANNING WHEN, WHAT AND HOW YOU COMMUNICATE..................................................... 16
ASSIGNING ROLES AND RESPONSIBILITIES...................................................................................... 16
Sample Responsibility Assignment Matrix using RACI ..................................................................................16
Sample Communication Matrix ................................................................................................................................17
Planning and monitoring for risk. ............................................................................................................ 17
Qualifying Risks............................................................................................................................................................... 18
In association with 3
Example of Risk Assessment Matrix .................................................................................................................... 18
Risk Assessment Matrix............................................................................................................................................. 18
THE EXECUTING PROCESS............................................................................................................................. 18
THE MONITORING AND CONTROLLING PROCESS ............................................................................. 19
VALIDATING AND CONTROLLING THE SCOPE................................................................................. 19
SCOPE CREEP................................................................................................................................................... 19
ADJUST FOR THE UNEXPECTED ............................................................................................................ 19
STATUS REPORTS.......................................................................................................................................... 19
Sample Status Report ..................................................................................................................................................20
THE CLOSING PROCESS................................................................................................................................... 21
Example Lessons Learned Report ......................................................................................................................... 22
Sample Self & Peer Assessment ............................................................................................................................. 23
KEY TERMS ............................................................................................................................................................24
PROJECT MANAGEMENT PORTFOLIO.....................................................................................................25
FURTHER READING ...........................................................................................................................................26
In association with 4
STEM RACING & THE PROJECT MANAGEMENT
EDUCATIONAL FOUNDATION
In 2020, STEM Racing partnered with the Project Management Institute Educational Foundation to integrate
project management into the competition. This guide supports teams in leveraging these skills for their STEM
Racing car and entry, with applications across various industries.
Andrew Denford, Founder and Chairman STEM Racing, says of the association with PMIEF:
“We’re delighted to welcome PMIEF as a partner of STEM Racing and look forward to a long and successful
relationship. Project management is fundamental in our Challenge, as the students have limited time and
resources for taking their STEM Racing entry from concept to reality and I’m sure that PMIEF will be able to
assist our students with this process. The scope of the partnership allows us to extend the learning and
training to STEM Racing staff and our In-Country Co-ordinators (ICCs) who deliver the programme
internationally, and I am sure there will be enormous benefit to both individuals and STEM Racing to have this
opportunity.”
The PMIEF Executive Directorship said of the relationship:
"Our partnership with STEM Racing supports its professionals to learn project management and, in turn, to
transfer that knowledge to young people by thoughtfully integrating it into this globally renowned Challenge.
The organization already appreciates the value of having youth learn through a highly experiential Challenge, so
we are confident this collaboration will only enrich their participation in this exciting, project-oriented
competition."
ABOUT PMIEF
PMI Educational Foundation (PMIEF) is a 501(c)(3) supporting organization of the Project Management Institute
(PMI), the world's leading not-for-profit professional membership association. Founded in 1990, PMIEF
cultivates long-term relationships with non-profits across the globe to help them integrate project
management in their youth programs and to build their own project management capacity. The foundation
achieves its mission to “enable youth to realize their potential and transform lives through project
management” and its vision for “inspiring youth to achieve their goals, making dreams a reality” by investing in
high-quality organizations that exemplify a commitment to preparing young people for 21st century success
and an appreciation for both the societal application and value of project management. Visit PMIEF.org for
more information.
ABOUT THE PROJECT MANAGEMENT
INSTITUTE
The Project Management Institute (PMI) is the world's leading association for those who consider project,
program, or portfolio management their profession. Through global advocacy, collaboration, education and
research, the PMI work to prepare more than three million professionals around the world for The Project
Economy: the coming economy in which work, and individuals, are organized around projects, products,
programs, and value streams. Now 50 years in the making, the PMI work in nearly every country around the
world to advance careers, improve organizational success and further mature the project management
profession through globally recognized standards, certifications, communities, resources, tools, academic
research, publications, professional development courses and networking opportunities. As part of the PMI
family, ProjectManagement.com creates online global communities that deliver more resources, better tools,
larger networks, and broader perspectives. For more information visit:
In association with 5
PMI.org
projectmanagement.com
@PMInstitute
https://www.linkedin.com/company/projectmanagementinstitute/
https://www.instagram.com/pmi_org/
PRINCIPLES OF PROJECT MANAGEMENT
You probably are already engaging in project management in your everyday life. Each time you plan for a
vacation, scheduled a time, and developed a budget for your group of friends to get together, prepared a
presentation or entered a competition with your team, you were participating in various aspects of project
management.
Project Management are processes followed to help ensure that all project work that must be completed to
create a product, service or result is understood, planned, and finished within the constraints of scope
(Description of product, service, or result boundaries and acceptance criteria), time (the schedule), cost (the
budget) and quality.
WHAT IS A PROJECT?
Perhaps it is best to say what a project is not… It is not a daily, weekly, or even monthly routine or activity
such as walking the dog or weekly chores. These activities are called ongoing operations. A project is
temporary, it has a beginning and end, and it creates a unique product, service, or result. It can vary in size, be
simple or complex and will involve resources such as materials and people. Some examples of a project are
hosting and planning a school prom, a birthday party, or your entry into STEM Racing.
KEY ROLES IN PROJECT MANAGEMENT
Project manager
This is the person responsible for making sure that each of the project’s goals and objectives are completed.
The project manager with leadership, influence, expertise, and communication skills oversees the project from
beginning to end, guides and works with the team to complete the scope, and ensures that everyone involved
is informed about how the project progressing. In an STEM Racing team this could be the Team Manager, or
you could create a Project Manager role within your team.
Project stakeholder
This is a person or an organisation who is involved or has an interest, positively or negatively, in the project or
the outcome of the project. Project stakeholders may include customers, clients, vendors, team members and
contributors to daily activities. All stakeholders need to be kept informed of the project’s progress. The
project stakeholders in STEM Racing could include your school or college, STEM Racing HQ or your incountry coordinator.
Project sponsor
This is a key project stakeholder and is the person that provides financial and other needed resources for the
project. The project sponsors in STEM Racing are your financial and in-kind sponsors or indeed your school
or college.
Project team members
These are the people who work on a project and contribute to its success. This is your STEM Racing team.
In association with 6
THE TRIPLE CONSTRAINTS OF PROJECT MANAGEMENT
Every time you start a project you will be concerned with what must be done (scope), how much it will cost
(budget), and how long it will take (time). You do this all the time, using the above examples of hosting and
planning the prom or a birthday party. We call the three parameters the triple constraints of project
management.
As a project manager you will want to define these parameters early in the project. Once defined, you will use
these parameters as guideposts as you plan and later execute your project. You will also determine which
parameter is most important and use the other two as negotiating points if necessary. For example, you might
determine the most important parameter is being ready for your regional competition (time) with a car that
meets the specifications (scope). If you run behind schedule, you might need more money or resources (cost)
to manufacture the car correctly and make it to the competition on time.
You will notice the parameter of quality in the middle of the triple constraints and resources and risks as
influencers. Quality, risks, and resources are used as references to attain your goals. You always need to keep
them in mind as you plan and execute.
In association with 7
THE PROJECT MANAGEMENT PROCESS
Any project, no matter the size or complexity, involves using specific skills, tools, and procedures to complete
the project’s goals. Project management can be broken down into five processes:
These processes help the project manager and team members define, organise, and keep track of all the work
that needs to be completed for a project to be successful.
OVERVIEW
The Initiating Process is the beginning of the project. During this process, project stakeholders are identified,
and a project manager is selected. Project goals and objectives are defined, and authorisation is obtained to
proceed with the project.
During the Planning Process, the project plan is created. The project manager and team members define
project and product scope, major deliverables, and exclusions; subdivide project deliverables and project work
into smaller components (Work Break Down). This information allows the team to define the activities and
tasks needed to complete the final product, service, or result. They also determine what staff and resources
that are needed and establish the timeline and available budget for the project. The planning process is very
important to the overall success of the project. Without careful planning, a project manager and project team
may find it very difficult to achieve project success.
Executing is the process of working through the project plan. The executing process involves performing the
activities outlined during the planning process.
Monitoring and Controlling occurs continuously throughout the entire project. Monitoring and controlling
involves ensuring that all the tasks in the project plan are completed to produce the deliverables and final
product of the project, as per the definition of the scope, on time and within budget, as well as addressing any
changes necessary to successfully achieve the project goals.
In the Closing Process, project goals are delivered. Final administrative work is completed, and lessons
learned are captured to improve future projects. The closing process involves taking the time to celebrate the
team’s successes along the way toward completion of the project.
Each of these processes will be addressed in more detail below:
In association with 8
INITIATING PROCESS
The initiating process group has three goals:
• Define the project
• Identify stakeholders
• Authorise the project by developing a project charter
DEFINING THE PROJECT
During this process you will define the goals and identify the deliverables of your STEM Racing competition
entry or as we will now call it your STEM Racing Project. You will need to answer the basic project questions
of Why, Who, What, When, Where and How:
WHY is the project being initiated? What is the reason for the project?
WHO is this work being done for? Identify the people participating in or affected by the project’s outcome
both positively and negatively.
WHAT are we going to deliver? What work do we need to complete? What resources and funds do we
need to produce these deliverables?
WHEN will we produce these deliverables? When will the project sponsor approve and accept the final
project deliverables?
WHERE will the deliverables be used?
HOW are we going to achieve the project’s goal and objectives? How will success be measured?
IDENTIFY THE STAKEHOLDER
Stakeholders are the people or organisations involved or that have an interest, positively or negatively, in the
project or the project’s outcome. A stakeholder register should be created which includes the individuals
involved and/or impacted by the project, their role in the project and their contact information.
Sample of a Stakeholder Register
Name Role in project Organisation Contact Engagement
Ms. Wang Teacher My School smith@school.com
A Singh Sponsor Sponsor Inc rharvey@sponsor.eu
A Denford Comp CEO STEM Racing info@f1is.com
S Ali Team member My Team millar@team.com
In association with 9
AUTHORISE THE PROJECT
A project charter is a document authorising the start of a project and is used to further clarify and refine the
project. It will describe the outcomes and expectations for the project and identify the measure of
performance, milestones, assumptions, constraints, and identify risks and resources.
The Why, Who, What, When, Where and How questions are used to create the project charter.
The project description outlines your goals. Goals should be specific, measurable, and observable. Goals can
guide a project from start to finish. The clearer you are in defining your goals, the easier it will be to stay on
track.
The project manager should be named, and a list created of the team members that will be involved in
the project.
The project reason/justification outlines the reason for doing this project. The why question could be ‘we
want to become World Champions’.
A milestone is an estimated time when a major deliverable will be completed. Consider when high-level
progress will be made throughout the project. For example, when your car will need to be completed.
The acceptance criteria documents and signed off by the customer the approval of the final deliverable or
product, indicating it meets the product or deliverable definition as a principal output of deliverables
verification developed as a control quality process.
Assumptions are factors about the project that you consider true without getting proof. Identifying
assumptions helps a team clarify assumptions that not all team members share. An assumption could be that
your school will excuse you from class to attend a final event.
A constraint is any factor that provides a limit on the ways that a project goal can be accomplished. This may
include limitations in finance, scheduling, people, or others. For example, a sponsor not paying would limit
finance or the new release of the technical regulations has increased the minimum weight of the car.
Risk includes any unexpected situations that might arise that may hamper your project. Consider potential
risks at the beginning and throughout a project so that you can manage them appropriately and create a plan of
response. While you cannot predict all situations, the more prepared you are, the more successful your
project will likely be. An example of a risk could be an issue with your 3D printer preventing you from printing
your car front wing. The response plan would be to have a list of contacts who have a 3D printer and would
be willing to let you use it.
Resources may include money, time, people, expertise, equipment, machinery, or a workplace. Consider all
resources that would be needed for the project and their estimated cost.
By taking the time in the beginning to define the project and obtaining authorisation, teams can set themselves
up for success. Once the project charter has been approved the project is authorised and can commence.
DELIVERABLES
These are the products, services, or results of a project or phase. In STEM Racing this will be your cars,
portfolio work, pit display etc. Deliverables are written as a statement of something accomplished or
produced and you should track their progress throughout the project.
MILESTONES
Milestones will always have at least one deliverable and will include the due date. This serves as a marker for
how far along you are in the project.
The Why, Who, What, When, Where and How are not yes/no questions. Instead, they are all openended questions. Asking open-ended questions helps get a fuller sense of what the project includes.
For example:
In association with 10
If your team asked, “Do we know who the project stakeholders are?” You might answer “Yes,” but it is
possible that each team member has different people in mind.
Asking an open-ended question like, “Who are the project stakeholders?” provides the opportunity for all
ideas.
SAMPLE PROJECT CHARTER


PROJECT CHARTER

Project: STEM Racing
Team name: Evolution
Date: September 15
Project manager
The person responsible for ensuring that each of the project’s goals and objectives are completed.
Team member
The people who work on a project and contribute to its success.
Project description
Describe the project. What is the goal of your project?
Project role/justification
Why are you doing this project?
Major milestones
What are the big points of progress? What are the deliverables? When are they due?
Acceptance criteria
How will the final product be evaluated?
Assumptions
What do you believe to be true about this project?
Constraints
What factors will limit how the project gets done?
Risk
What things could cause issues during the project?
Resources
What resources are needed? What will it cost?
Project Start date XX/XX/XXXX End Date XX/XX/XXXX
Project Manager Signature Date XX/XX/XXXX
Approved by Signature Date XX/XX/XXXX
In association with 11
PLANNING PROCESS
The planning process includes the following actions:
• Writing a scope statement
• Developing the WBS (Work Breakdown Structure)
• Building a project schedule
• Planning for acquiring resources
• Creating a budget
• Assigning roles and responsibilities
• Planning how and when to communicate
• Planning for risk
• Planning how to monitor and control the project
WRITING A SCOPE STATEMENT
Tip: Common creative thinking techniques include brainstorming and mind mapping.
The scope statement builds upon the description created in the project charter in the initiating process.
It sets the goals for what will be accomplished in your project. Aim to make your goal as specific as possible
and measurable so you can determine if your goals are achieved.
A project scope statement describes the work that will be done and what will not be done to create the
project’s unique outcome.
For example, you know you will need to prepare a verbal presentation, engineering portfolio and build a pit
display so these items must appear in the scope statement. You also know that STEM Racing is a team
competition so no individual work needs to be submitted and individual work would not appear in the scope
statement. You should read the competition regulation carefully and list all the deliverables you are going to
be expected to deliver. These are your guidelines and standards.
DEVELOPING THE WBS / PLANNING FOR QUALITY
Work Break Down is one of the most important documents. It is developed in the planning phase. It is defined
in the PMBOK as a hierarchical decomposition of the total scope of work to create the project deliverables.
The WBS is the foundation to define the activities to develop the schedule. It allows the creation of the
budget, estimating the activities cost, the work package's main components, and the deliverables. It permits the
definition and link of the resources with the activities, identification of risk for the project and requirements
and necessities of the people to protect them from harmful activities during the execution.
The WBS partnering with the project scope statement forms the scope baseline. This baseline is the
fundamental part of scope validation to obtain the acceptance deliverable document signed by the client.
The WBS is developed using only noun words, and every branch goes from the general to the description; for
example, the car body is at the general level or top to the level, design of the car body. The level is called the
work package; it represents all the activities involved in designing and calculating the car body.
A technique you can use to verify that the quality standards have been met is called acceptance criteria. You
can define acceptance criteria for the entire project or specific deliverables. Since acceptance criteria identified
are designed to effectively assess your tasks, they should be qualitatively or quantitatively specific. Stating to
accept a car race within 1 second only does not help much. The below example demonstrates the quality
acceptance criteria that could be implemented for your car development.
In association with 12
Sample Quality Acceptance Criteria
Quality Acceptance
Criteria
Testing and
Assessment
When? Person
Responsible
Review, Acceptance
and Sign Off
Project Management
Portfolio is of High
Quality
Review with
Scorecard
Criteria and
Marketing/
Branding Team
4 Weeks before due
Date
Project Manager Team Principal/
Project Manager
No component
breakages.
Visual signs of
cracking checks.
At end of first and
second round of
testing
Manufacturing
Engineer
Team Principal
PLANNING WHEN AND HOW TO MONITOR AND CONTROL
Each part of the planning process builds on the others. You may find that you need to revisit and revise parts
of your project along the way. This process of review and revision is part of monitoring and controlling your
project. Monitoring and controlling will be easier to conduct with ongoing check-ins.
Take a moment to plan how frequently you will schedule check-ins with your team and project sponsor and
how you will document the progress you are making. You may decide to check in hourly, daily, or weekly.
BUILDING A PROJECT SCHEDULE - per each deliverable of the WBS and the project
A project schedule needs to be created, identifying all the activities that part of the work packages in the
WBS to be completed including their start and due dates. The following steps should be undertaken:
DETERMINE THE MAJOR CATEGORIES OF WORK:
These categories can be established in several ways.
1. By PHASES: What should be accomplished pre competition, during competition, etc?
2. By MAJOR PIECES OF WORK: what should be accomplished for the design of the car, the
manufacture of the car, creation of the enterprise portfolio, etc.
3. By MILESTONE: Milestones are the critical points in a project's timeline that can be monitored to
determine if the project is on schedule. They show completion of major pieces of the project.
DEFINE TASKS:
What tasks need to be accomplished to meet each milestone? Tasks are activities that are the “to-do” list.
Breaking out the categories and tasks in this way is called a Work Breakdown Structure (WBS). Make
sure that the degree of decomposition of components is appropriate.
In association with 13
SAMPLE OF A WORK BREAKDOWN STRUCTURE
DETERMINE THE SEQUENCE
When will each task be accomplished? To establish this sequence, assess task dependencies.
A dependent task requires completion of another task before it can begin. For example, designing your car in
CAD must be done before manufacturing. For dependent tasks, be especially careful with the timeframe of the
task before it to ensure your project remains on track.
An independent task can be completed at any time and is not related to the completion of another task.
ESTIMATE TIME
How long will each task take? Make your best estimate based on experience or team discussions.
Underestimating time is a common error. Including extra time in the schedule ensures you have the needed
time to complete your project on time.
As you will be attending an event final you have a hard deadline that cannot be moved. Running out of time
could mean not finishing your car or other judged work.
BUILD THE SCHEDULE
With the above information, you can now build the schedule. The critical path is like the main route through a
project, showing the longest path and the quickest way to finish. If anything slows down on this path, it will
make the whole project take longer.
A Gantt chart a bar chart that shows a schedule. On the chart, activities are listed on the vertical axis, dates
are on the horizontal axis and the time it takes to do each activity is shown as horizontal bars.
Various tools, such as tables in Word, charts in Excel, or project management software like Asana, JIRA,
Microsoft Project, Miro, Monday, Smartsheet, Trello, or projectmanager.com, can be used to create your
schedule. Check with your school to determine the accessible tools.
In association with 14
SAMPLE SCHEDULE
In association with 15
PLANNING FOR AQUIRING RESOURCES
Resource planning considers all the elements needed to complete the project, such as people, money,
equipment, or space. Managing resources are essential to enhance project's overall efficiency and profitability.
In the planning process, determine where and how you will acquire each resource, when it is needed, and for
how long.
Resource Management: Project resources are acquired, allocated, monitored, and controlled.
Tip: In STEM Racing, resources play a vital role in racing car research and development, pit display production, etc. For
instance, in R&D, engineers strategically acquire resources such as bearings and 3D printing services. The decisions of
WHEN, WHAT, HOW, and HOW MUCH to acquire these resources, based on budget, utilization, quality, and other
factors, form the foundation for the smooth execution of car design, testing, and manufacturing. Inconsiderate planning
could lead to deadlines being pushed back.
Sample Resource planning
Resource Needed When will you need it? How you will acquire it
Model block November 15 Place order with Denford LTD
Denford CNC router November 24 (1day) Request access via school lab
technician
School Minibus January 20 (2 days) Book Minibus with School
administration office

CREATING A BUDGET
A budget is a financial plan for income and expenditure over a defined period. The best technique to create a
budget is using the bottom-to-top technique in the WBS to estimate the cost of every work package until the
top, the deliverable. The WBS will allow us to attach resources, equipment, and materials to complete every
work package and its corresponding deliverable.
You will need to:
• Identify what items will cost you money and how much they will cost. It is normal for costs to initially
be estimated and your budget should include the actual costs so you can identify any over or under
spend.
• Identify where you plan to acquire the money, e.g. A fundraising event, sponsor pitch or a donation.
• Agree who will be responsible for the budget and keep a record of spending and approve any
purchases.
There can be many different costs associated with an entry to STEM Racing, some of which may not be
immediately obvious or expected. For example, they may be associated with risks you have identified or
unexpected changes that you need to make as you develop your car. There may also be a scenario where
items cost more than you expected, and you need to ensure your budget can accommodate all these. In
finance this is called the budget contingency. You can decide how much contingency you need by assessing
how likely each of the scenarios presented above are likely to happen.
In association with 16
Sample Budget
STEM Racing Budget
Resource Budget cost Actual cost Difference
Equipment
Travel
Materials
Contingency
Tip: Budget Management can also be illustrated in pie charts, bar charts, etc., depending on what you would
like to show. You might want to consider including the Project’s Cash Flow.
PLANNING WHEN, WHAT AND HOW YOU COMMUNICATE
Team members and stakeholders need information on the project's development and potential changes to
complete the work.
Planning communication involves understanding who needs to communicate, how often, and what information
is relevant to each stakeholder.
ASSIGNING ROLES AND RESPONSIBILITIES
Assess the strengths, skills, and abilities of each team member to assign responsibilities effectively. Use a
Responsibility Assignment Matrix (RAM). A legend or key is usually applied to the RAM, the one most used is
known as RACI (Responsible - Accountable - Consulted – Informed), to assign team members to tasks.
Sample Responsibility Assignment Matrix using RACI
Task Team Principal
/Project
Manager
Design
Engineer
Manufacturing
Engineer
Graphic
Designer
Design Car using Autodesk Accountable Responsible Consulted Informed
Design Team Logo Accountable Consulted Informed Responsible
Create Budget Accountable Informed Informed Informed
Book CNC Time Accountable Consulted Responsible -
Legend / Key:
Responsible for doing the work
Accountable for making sure the work gets done
Consulted to provide critical input to the work
Informed of the work being done or completed
An STEM Racing team will be very structured, the rules and regulation documents highlight the roles that a
team should have. This does not limit you assigning other roles to team members.
It is important to ensure that each activity and task identified in the project schedule is allocated to a team
member.
In association with 17
Sample Communication Matrix
Who to contact What to
communicate
Communication
method
When
Teacher Milestones met Face to Face Milestone completion
STEM Racing HQ Competition registration Email / on-line forms Start of year and when
information is requested
Sponsors Competition progress
update
Newsletter Email Monthly
Team members Team update Microsoft Teams Daily @ lunchtime
It is very important to have an internal project team communication plan. You should agree how you plan to
communicate, how often, where, and when. Look at the various communication tools that are available to you
in case you cannot always meet in person and weigh up the advantages of different platforms for different
tasks.
Planning and monitoring for risk.
The objective is to identify two kinds of risks. The first might impact the project's triple constraints (scope,
schedule, and cost); the second type of risk might affect the safety of people and the environment.
Risk Identification
Risk Analysis and Assessment
Risk Response
Continue to Monitor Risks
The efficient form to identify risks is using the WBS.
WBS outlines the systematic approach to managing risks, from identification to response and continued
monitoring, as well as the classification and assessment of risks based on their impact and probability. The main
idea is to evaluate each component (work packages from the bottom to the top of the WBS).
Risks can be negative or positive.
Risk Responses for threats that may have a negative impact include Accept, Avoid, Escalate, Mitigate or
Transfer.
Risk Responses for Opportunities that may have a positive impact include Accept, Enhance, Escalate, Exploit or
Share.
Risks could affect various areas of the project, including:
• Resources: Ability to acquire people, equipment, funding, or other resources to complete project. All of
these apply to STEM Racing.
• Timing: Will deliverables or the entire project be completed on schedule? This is critical for STEM
Racing as you have a hard deadline of attending an F1 in School final event.
• Scope: Completing and delivering all the items named in the original scope. You may choose to change
the class of the competition you have entered.
• Quality: How well each deliverable meets the goals set in the acceptance criteria. Has your car been
manufactured as expected?
In association with 18
Qualifying Risks
All identified risks are important and valuables to successfully complete the project. However, not all risks are
having the same level of importance or urgency. Thus, classified risks due to their impact over the triple
constrain (Scope, Time, cost) is particularly important.
Example of Risk Assessment Matrix
Risk Assessment Matrix
What is the
Risk
Threat or
Opportunity?
Risk Impact
L = Low
M =
Medium
H = High
Risk
Probability
Risk
Score
Area of Impact
R = Resource
T = Timing
S = Scope
Q = Quality
Risk Response
Additional
Testing
Resources
made available
to the Team
Opportunity L M M R - Additional
Resources
made available
Q: Shorter
cycles to
improve our
car
Enhance:
- Book
additional
Testing Time
- Update car
manufacturing
schedule
Car front
wing damaged
during testing
Threat M L M R – New part
will need to be
manufactured
T – We may
not have
enough time to
manufacture a
new wing
before the
finals
Mitigate
-Manufacture a
spare wing
-Ensure testing
takes place
well before the
finals
Tip: For the Risk Impact, Probability and Score, you may choose to use a quantitative scale, i.e. 1 - 5 to measure risk.

THE EXECUTING PROCESS
Executing is the process of working through the project plan. This involves putting your project plan into
action. The project plan serves as a guide to help ensure that the deliverables — the intended goals of the
project — will be completed properly, on time, and within the budget.
As work is being executed, you should strive to:
✓ Use your budget and resources as planned.
✓ Manage the risks you identified.
✓ Stay focused only on the work you described in your project’s scope.
✓ Meet your milestones.
In association with 19
✓ Document your progress in an organised way.
✓ Communicate your project’s progress regularly and effectively to your stakeholders.
✓ Update any component of the initial project management plan if needed
By checking on your progress, evaluating whether project goals are being achieved in the best possible way and
being prepared to adjust their path, if necessary, you are engaged in the monitoring/controlling process.
THE MONITORING AND CONTROLLING PROCESS
Monitoring/controlling is a continuous process throughout the project life cycle. Project managers and
team members need to establish a cycle to evaluate the progress of the project and report back to
stakeholders about project developments.
VALIDATING AND CONTROLLING THE SCOPE
This is a key component of the monitoring/controlling process group.
Keep the following in mind:
• Ensures that all the tasks necessary to achieve the project goals are completed.
• Identify if any activities need to be added to the project.
• Prevent work on the project from going beyond the scope.
• Determine what to do if any activity is taking more time than planned.
SCOPE CREEP
This occurs when work is added to the project without appropriately adjusting the schedule and resources,
and without obtaining sponsor approval.
Routinely review the Acceptance Criteria that were established in the project to make sure that the
products of a project will satisfy project stakeholders’ needs and meet their standards.
Avoiding scope creep should start early in the project, ideally during the initiating process when you
established a goal and set the boundaries for the project’s work and scope. During the planning process you
established what would not be included or would be “out of scope” for the project. If you establish early what
is and what is not a part of the project’s scope you can rely on and monitor those plans to help you avoid
scope creep.
ADJUST FOR THE UNEXPECTED
It is more than likely that you will encounter some surprises as the project progresses. This is OK, it is what
monitoring and controlling is for. Discuss any surprises that occur as project work is being done. If a change
needs to occur, review the schedule, resources, and scope to see if there are other changes that need to be
made.
STATUS REPORTS
A status report is an effective way to monitor and document of the progress of your project — and to
communicate that progress to others. Each status report should include:
✓ What work has been completed
✓ What tasks are in progress
✓ What work is still planned
In association with 20
✓ What issues have developed
Status reports can help identify items that might affect the project scope, timeline, budget, or deliverables. For
example, if you raise money to buy a 3D printer but this arrives 2 weeks late, this will affect your timeline and
you may not have time to 3D print your wheels for the regional final.
Sample Status Report

Status Report
Project: STEM Racing
Team name: Evolution
Date: November 12
Project status: in good shape
Tasks accomplished:
- All sponsorship acquired.
- Car CAD design milestone achieved and car ready for cfd analysis and then manufacture.
Tasks in progress:
- CFD analysis underway.
- Manufacturing engineer is preparing resources (model blocks) and booking the Denford CNC router to cut the
car.
Planned tasks
- Portfolio writing.
- Verbal presentation script writing and presentation creation.
Issues:
- One of the team members has an appointment clash on the date of the regional final. They are currently
attempting to reschedule the appointment.
- Our 3D printer needs maintenance, and we are yet to confirm an engineer site visit.
Questions for discussion:
- We need to finalise our transport arrangements for attending the finals.
In association with 21
THE CLOSING PROCESS
Closing is the process of completing the project. Finishing a project is an accomplishment. It is the
achievement of a lot of work. As a group, you and your team members collectively sparked an idea, planned it,
executed the plan, monitored/controlled your progress, and have now reached the closing process.
In the closing process you can reflect upon the quality of the project deliverables, what you learned about
managing a project, and how well you and your team worked together.
In the closing process there is still some work to be completed as follows:
✓ A closing presentation is created, for some projects, to present the final report to the stakeholders.
✓ Collect and store any project-related paperwork and documents (such as the project plan, completed
schedule, etc.) in a project portfolio such as in a notebook or a computer. These documents
become reference material for future projects.
✓ Team members need to “sign off” on the project to verify that the project is completed.
✓ Create a Lessons Learned document with team members by asking what went well, what could
have been done better, and what should continue. You may have received feedback from the judges
which should be included. You can also reflect on how your car performed on the track.
✓ Complete a self and peer assessment. Include whether you and your group:
o Treated each other with respect,
o Shared responsibilities,
o Communicated clearly and effectively,
o Worked in an organized fashion and
o Managed time wisely.
✓ Finally, celebrate all that you and your team have accomplished! Regardless of the outcome, you
have dedicated time and effort, learned a lot along the way, and should be rewarded for such effort.
In association with 22
Example Lessons Learned Report

Lessons Learned

Project: STEM Racing
Team name: Evolution
Date: January 15
What did we do right?
- We won the regional final and have a place at the national finals.
What could we have done better?
- We have not scored well in our verbal presentation. We all acknowledge we did not rehearse this enough.
- Our car was not as fast as we had hoped. We all acknowledge that we did not leave enough time to test our
prototypes.
What should we continue to do?
- Test, test, test
- Verbal presentation script writing, this really helped
What significant issues did we encounter and how did we resolve?
- Our 3d printer really let us down
- We built a relationship with our local university to gain access to their equipment
What are our lessons learned?
- We need to use as much time as we can analysing our cad design. Our car was fast, but we wanted to win
the fastest car award
- We should have had more team meetings especially as we progressed through the project milestones
In association with 23
Sample Self & Peer Assessment
SELF AND PEER ASSESMENT

PROJECT: STEM Racing
TEAM NAME: Evolution
DATE: JANUARY 15
List your team’s members, including yourself, in the space provided below. Then, rate every person on each
behaviour listed.
4 = Always 3 = Usually 2 = Sometimes 1 = Never

Team Member Names
(including your own)
Behaviours

Exhibited a positive attitude
Treated other with respect
Shared responsibilities
Did work accurately & completely
Communicated clearly & effectively
Was organized
Managed time wisely
In association with 24
KEY TERMS
INITIATING PROCESS
Acceptance criteria: A set of conditions that is required to be met before deliverables are accepted.
Assumption: A factor in the planning process that is true, real, or certain, without proof or
demonstration.
Constraint: A limiting factor that affects the execution of a project,
program, portfolio, or process.
Deliverables:
Any unique and verifiable product, result, or capability to perform a service that is
required to be produced to complete a process, phase, or project.
Milestone: A type of schedule that presents milestones with planned dates.
Project charter:
A document issued by the project initiator or sponsor that formally authorises the
existence of a project and provides the manager with the authority to apply
organisational resources to project activities.
Project scope: The work performed to deliver a product, service, or result with the specified
features and functions.
Resource: A team member or any physical item needed to complete the project.
Risk: An uncertain event or condition that, if it occurs, has a positive or negative effect on
one or more of the project objectives.
Stakeholder register: A project document including the identification, assessment, and classifications of
project stakeholders.
Negative interest:
A stakeholder with negative interest is typically one who is affected by the
outcomes of a project. They either do not want that outcome to happen or will be
negatively impacted by that outcome.
PLANNING PROCESS
Milestone: A significant point or event in a project, program, or portfolio.
Planning process:
Those processes required to establish the scope of the project, refine the
objectives, and define the course of action required to attain the objectives that the
project was undertaken to achieve.
Project schedule: An output of a schedule model that presents linked activities with planned dates,
durations, milestones, and resources.
Scope: The sum of the products, services, and results to be provided as a project.
Work Breakdown
Structure (WBS):
A hierarchical decomposition of the total scope of work to be carried out by the
project team to accomplish the project objectives and create the required
deliverables.
Gantt Chart
A bar chart provides schedule information where activities are listed on the vertical
axis, dates are shown on the horizontal axis, and activity durations are shown as
horizontal bars placed according to start and finish dates.
Critical Path The sequence of activities that represents the longest path through a project, which
determines the shortest possible duration.
Responsibility
Assignment Matrix
(RAM)
This matrix is a grid that shows the project resources assigned to each work
package. A RACI chart is a common way of showing stakeholders who are
responsible, accountable, consulted, or informed and are associated with project
activities, decisions, and deliverables.
Budget A financial plan for income and expenditure over a defined period.
In association with 25

EXECUTING / MONITORING / CONTROLLING
Communications
management:
A component of the project, program, or portfolio management plan that describes
how, when, and by whom information about the project will be administered and
disseminated
Executing process: Those processes performed to complete the work defined in the project
management plan to satisfy the project requirements.
Monitoring/controlling:
The processes required to track, review, and regulate the progress and
performance of the project; identify any areas in which changes to the plan are
required; and initiate the corresponding changes.
Risk: An uncertain event or condition that, if it occurs, has a positive or negative effect on
one or more project objectives.
Scope creep: The uncontrolled expansion to product or project scope without adjustments to
time, cost, and resources.
Status Report A report on the current status of the project.
CLOSING PROCESS
Closing process: The process(es) performed to formally complete or close a project, phase, or
contract.
Lessons Learned:
The knowledge gained during a project which shows how project events were
addressed or should be addressed in the future for the purpose of improving future
performance.
PROJECT MANAGEMENT PORTFOLIO
Project Management
Assessment
Suggest Checklist
Initiation Process ✓ Kick Off Meeting
✓ Project Charter
✓ Scope Statement
✓ Quality Acceptance Criteria
Project Schedule ✓ Work Breakdown Structure (WBS)
✓ Schedule
✓ GANTT Chart
Budget and Resource
Management
✓ Resource Management
✓ Budget Expenditure Tracking (Baseline vs. Actual)
Roles and Responsibilities ✓ Role Descriptions
✓ Team Structure
✓ RACI Chart
Team & Stakeholder
Communications
✓ Communication Plan (Internal and External)
✓ Communication Tools
✓ Stakeholder Register
Risk Management ✓ Risk Identification, Planning, Analysis and Assessment
✓ Risk Register Impact and Probability
Monitoring & Controlling ✓ Status Report
✓ Scope Creep
✓ Sign Off

Tip: Other areas to consider
Initiation Process: Mission/ Vision/ Goals, Key Deliverables and Out of Scope
In association with 26
Project Schedule: Critical Path, Major Milestones and PERT Analysis
Budget and Resource Management: Budget/ Resource Strategy, Income vs. Expenditures and Cash Flow.
Roles and Responsibilities: Team Dynamics/ Assessment, Ownership of Deliverables, Culture and Motivations.
Team & Stakeholder Communications: Power – Interest Grid and Methods of Communications
Risk Management: Risk Assessment Matrix
Monitoring & Controlling: Change Management, Lessons Learned, Strategy and Key Performance Indicators.
FURTHER READING
For more resources and information about project management, head to the resources page of the STEM
Racing website:
F1INSCHOOLS.COM
RULES AND REGS
PMIEF PROJECT MANAGEMENT SKILLS FOR LIFE
AGILE PRACTICE GUIDE
KICK OFF
Project Management: Agile, Predictive, and Hybrid
Managing a project is like guiding a ship. Depending on your destination and the weather, there are different
ways to steer it. Let's explore three methods: Agile, Predictive, and Hybrid.
Agile: Flexible and Fast
Agile is like building a Lego castle without a fixed plan. You start, get feedback, and keep adding pieces. It's
great for projects that change a lot, like making an app.
Key Points: Flexible, iterative, teamwork focused.
Predictive: Plan It All
Predictive is like following instructions to build a model airplane. You plan everything and stick to it, perfect
for projects with clear steps, like constructing a building.
Key Points: Detailed planning, steady progress, less flexibility.
Hybrid: Uncertainty or risk around Requirements
Hybrid mixes Agile and Predictive. It's like baking a cake using a recipe but adding your choice of toppings. You
have a plan but can tweak it. This approach suits projects needing structure and some adaptability.
Key Points: Combines methods, flexible planning, balanced.
Conclusion: Choosing a project management method depends on your project's needs. Agile lets you
adapt quickly, Predictive keeps you on a set path, and Hybrid offers a middle ground. It's like picking the best
route for your ship, ensuring a successful journey!

 Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 2 of 54 23 April 2025
Front Cover – evolut1on, Germany, Aramco STEM Racing™ 2024 World Champions
CONTENTS
ARTICLE C1 – DEFINITIONS ....................................................................................................................................................6
C1.1 WORLD FINALS EVENT ..............................................................................................................................................6
C1.2 STEM RACING™ IN-COUNTRY CO-ORDINATOR (ICC) .................................................................................................6
C1.3 PARC FERMÉ.............................................................................................................................................................6
C1.4 COMPETITION PROGRAMME .......................................................................................................................................6
C1.5 WORLD FINALS TERMS AND CONDITIONS FOR ENTRY....................................................................................................6
C1.6 KEY PERFORMANCE INDICATORS (KPI’S).....................................................................................................................6
C1.7 CAR RACE TIME VALUE...............................................................................................................................................6
C1.8 TOTAL RACE TIME VALUE............................................................................................................................................6
C1.9 REACTION TIME VALUE...............................................................................................................................................6
C1.10 PROJECT ELEMENTS..................................................................................................................................................7
C1.11 RACE EVENT .............................................................................................................................................................7
C1.12 ENGINEERING DRAWINGS...........................................................................................................................................7
C1.13 RENDERINGS ............................................................................................................................................................7
C1.14 TEAM DIGITAL UPLOAD FOLDER .................................................................................................................................7
C1.15 PARTNERSHIPS .........................................................................................................................................................7
ARTICLE C2 – GENERAL INFORMATION ...............................................................................................................................8
C2.1 COMPETING TEAMS ...................................................................................................................................................8
C2.2 RETURNING STUDENTS..............................................................................................................................................9
C2.3 COMPETITION PROGRAMME, TEAM NUMBER AND TEAM NAME ........................................................................................9
C2.4 TEAM RESPONSIBILITIES ..........................................................................................................................................10
C2.5 ROLE AND RESPONSIBILITY OF ICC AND SUPERVISING TEACHER/ADULT.......................................................................10
C2.6 REGULATIONS DOCUMENTS......................................................................................................................................10
C2.7 INTERPRETATION OF THE REGULATIONS ....................................................................................................................10
C2.8 SUPPLEMENTARY COMPETITION REGULATIONS ..........................................................................................................11
C2.9 DESIGN IDEAS AND REGULATION COMPLIANCE QUERIES .............................................................................................11
C2.10 TEAM PARTNERSHIPS ..............................................................................................................................................11
C2.11 MANDATORY PROJECT ELEMENTS REQUIRED FOR WORLD FINALS ENTRY ....................................................................11
C2.12 TEAM REGISTRATION ...............................................................................................................................................15
C2.13 SUBMISSION OF PROJECT ELEMENTS ........................................................................................................................15
C2.14 PROJECT ELEMENTS TO BE RETAINED BY STEM RACING™ ........................................................................................16
C2.15 BENEFIT OF DOUBT..................................................................................................................................................16
C2.16 SPIRIT OF THE COMPETITION ....................................................................................................................................16
C2.17 PLAGIARISM............................................................................................................................................................16
ARTICLE C3 – COMPETITION AND JUDGING FORMAT.......................................................................................................17
C3.1 COMPETITION PROGRAMME......................................................................................................................................17
C3.2 JUDGING CATEGORIES .............................................................................................................................................17
C3.3 JUDGING SCORECARDS............................................................................................................................................17
C3.4 WORLD CHAMPIONS................................................................................................................................................17
C3.5 POINT ALLOCATIONS................................................................................................................................................18
C3.6 CLASSIFICATION OF TECHNICAL REGULATIONS...........................................................................................................19
ARTICLE C4 – SPECIFICATION & SCRUTINEERING JUDGING (160 POINTS)....................................................................20
C4.1 WHAT WILL BE JUDGED? ..........................................................................................................................................20
C4.2 TEAM PREPARATION ................................................................................................................................................20
C4.3 WHO NEEDS TO ATTEND?.........................................................................................................................................20
C4.4 JUDGING PROCESS/PROCEDURE...............................................................................................................................20
C4.5 SAFE/FIT TO RACE FIX .............................................................................................................................................21
C4.6 SPECIFICATION JUDGING DECISION APPEALS .............................................................................................................21
ARTICLE C5 – DESIGN & ENGINEERING JUDGING (180 POINTS)......................................................................................22
C5.1 WHAT WILL BE JUDGED? ..........................................................................................................................................22
C5.2 TEAM PREPARATION ................................................................................................................................................22
C5.3 WHO NEEDS TO ATTEND?.........................................................................................................................................22
C5.4 JUDGING PROCESS / PROCEDURE .............................................................................................................................22
C5.5 DESIGN & ENGINEERING PORTFOLIO REQUIREMENTS ................................................................................................22
ARTICLE C6 – PROJECT MANAGEMENT JUDGING (90 POINTS).......................................................................................23
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 3 of 54 23 April 2025
C6.1 WHAT WILL BE JUDGED? ..........................................................................................................................................23
C6.2 TEAM PREPARATION ................................................................................................................................................23
C6.3 WHO NEEDS TO ATTEND?.........................................................................................................................................23
C6.4 JUDGING PROCESS / PROCEDURE .............................................................................................................................23
C6.5 PROJECT MANAGEMENT PORTFOLIO REQUIREMENTS.................................................................................................23
ARTICLE C7 – ENTERPRISE JUDGING (180 POINTS)..........................................................................................................24
C7.1 WHAT WILL BE JUDGED? ..........................................................................................................................................24
C7.2 TEAM PREPARATION ................................................................................................................................................24
C7.3 WHO NEEDS TO ATTEND?.........................................................................................................................................24
C7.4 JUDGING PROCESS / PROCEDURE .............................................................................................................................24
C7.5 ENTERPRISE PORTFOLIO REQUIREMENTS..................................................................................................................25
C7.6 PIT DISPLAY SETUP AND PARAMETERS......................................................................................................................25
ARTICLE C8 – VERBAL PRESENTATION JUDGING (140 POINTS) .....................................................................................27
C8.1 WHAT WILL BE JUDGED? ..........................................................................................................................................27
C8.2 TEAM PREPARATION ................................................................................................................................................27
C8.3 WHO NEEDS TO ATTEND?.........................................................................................................................................27
C8.4 JUDGING PROCESS / PROCEDURE .............................................................................................................................27
C8.5 VERBAL PRESENTATION JUDGING PROVISIONS...........................................................................................................28
C8.6 VERBAL PRESENTATION VIDEO RECORDINGS .............................................................................................................28
ARTICLE C9 – RACING (250 POINTS) UNDER REVIEW.......................................................................................................29
C9.1 WHAT RACES WILL BE CONDUCTED? .........................................................................................................................29
C9.2 TEAM PREPARATION ................................................................................................................................................29
C9.3 WHO NEEDS TO ATTEND?.........................................................................................................................................29
C9.4 REACTION RACE PROCEDURE...................................................................................................................................29
C9.5 REACTION RACE SCORING........................................................................................................................................30
C9.6 TIME TRIAL RACE SCORING.......................................................................................................................................30
C9.7 KNOCK-OUT COMPETITION.......................................................................................................................................31
C9.8 DNF (DID NOT FINISH) RACE RESULTS......................................................................................................................32
C9.9 FALSE STARTS........................................................................................................................................................32
C9.10 TRACK, TETHER LINE AND TIMING SYSTEM INFORMATION ............................................................................................32
C9.11 CAR DECELERATION SYSTEMS.................................................................................................................................32
C9.12 RACE POWER PACKS ..............................................................................................................................................33
C9.13 CAR WEIGHT CHECKS ..............................................................................................................................................33
C9.14 JUDGES HANDLING CARS .........................................................................................................................................33
ARTICLE C10 – CAR REPAIRS AND CAR SERVICING.........................................................................................................34
C10.1 CAR REPAIRS..........................................................................................................................................................34
C10.2 CAR SERVICING.......................................................................................................................................................34
ARTICLE C11 – PROTESTS....................................................................................................................................................35
C11.1 SCRUTINEERING DECISION APPEALS .........................................................................................................................35
C11.2 SUBMITTING A PROTEST...........................................................................................................................................35
C11.3 UNSUCCESSFUL PROTESTS......................................................................................................................................35
ARTICLE C12 – JUDGES........................................................................................................................................................36
C12.1 OVERVIEW..............................................................................................................................................................36
C12.2 CHAIR OF JUDGES...................................................................................................................................................36
C12.3 THE JUDGING TEAMS ...............................................................................................................................................36
C12.4 JUDGING DECISIONS................................................................................................................................................36
ARTICLE C13 - AWARDS .......................................................................................................................................................37
C13.1 AWARDS CELEBRATION ...........................................................................................................................................37
C13.2 PARTICIPATION RECOGNITION ..................................................................................................................................37
C13.3 PRIZES AND TROPHIES ............................................................................................................................................37
C13.4 LIST OF AWARDS TO BE PRESENTED..........................................................................................................................37
APPENDIX… ...........................................................................................................................................................................38
AWARDS MATRIX ...................................................................................................................................................................39
SCRUTINEERING JUDGING SCORECARD...................................................................................................................................40
DESIGN & ENGINEERING SCORECARD .....................................................................................................................................41
PROJECT MANAGEMENT SCORECARD .....................................................................................................................................42
ENTERPRISE SCORECARD ......................................................................................................................................................43
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 4 of 54 23 April 2025
PIT DISPLAY & TEAM IDENTITY SCORECARD ............................................................................................................................44
VERBAL PRESENTATION SCORECARD......................................................................................................................................45
SPECIFICATIONS SCORECARD ................................................................................................................................................46
RACE PROCEDURE & TROUBLESHOOTING FLOWCHART ............................................................................................................51
PIT DISPLAY REFERENCE DIMENSIONS....................................................................................................................................52
PHYSICAL PROJECT ELEMENT SUBMISSION CHECKLIST............................................................................................................53

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 5 of 54 23 April 2025
Please note: any amendments made prior to the event will be indicated using red strikethrough
text. New text will be indicated using blue text.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 6 of 54 23 April 2025
ARTICLE C1 – DEFINITIONS
C1.1 World Finals Event
The World Finals event is managed by STEM Racing™ and is held over several days to
include various programmed social and competition activities. The event aims to provide all
participants with an educational and personal development ‘Experience of a Lifetime’.
Specifically, the competition aims to determine the World Champions of STEM Racing™
according to the 2025 STEM Racing™ World Finals Technical and Competition regulations.
C1.2 STEM Racing™ In-Country Co-ordinator (ICC)
Person/s and/or an organisation approved by STEM Racing™ to manage and co-ordinate
STEM Racing™ within a specified country or region of the world.
C1.3 Parc fermé
A secure area where all submitted cars and components are held to prevent unauthorised
handling but to allow technical inspections to be conducted by the Judges. (Literal meaning
in French of ‘closed park’).
C1.4 Competition Programme
The competition programme will detail the schedule of judging activities for all teams.
C1.5 World Finals terms and conditions for entry
This is a document issued by STEM Racing™ which constitutes an agreement between
STEM Racing™, ICC’s and supervising teachers regarding participation by teams in the World
Finals event.
C1.6 Key performance indicators (KPI’s)
These are portions of text that feature on the scorecards within a corresponding points range.
The KPI’s describe the type of evidence the Judges will be looking for in order to score the
team appropriately.
C1.7 Car race time value
A ‘car race time’ value is the actual time taken for a STEM Racing™ car to travel the track
from start to finish, measured from the instant the start box fires to when the car breaks the
finish line timing beam. In the case of reaction races, the ‘car race time’ value is calculated as
the ‘total race time’ value displayed on the electronic start gate minus the ‘reaction time’ value
displayed for that race.
C1.8 Total race time value
The ‘total race time’ value is displayed in the total time field on the electronic start gate at the
conclusion of every race. This time is the sum of the ‘car race time’ value and any ‘reaction
time’ value displayed on the electronic start gate.
C1.9 Reaction time value
A ‘reaction time’ value is the time recorded from the instant the five (5) start lights extinguish
to the instant the start trigger is activated by the driver. This value is displayed in the reaction
time field on the electronic start gate.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 7 of 54 23 April 2025
C1.10 Project elements
These are any materials and resources that the team presents as part of its entry for any
judging activity.
C1.11 Race event
The World Finals competition includes three separate race events. These are: Reaction
Racing 1, Reaction Racing 2, and Knock-out Racing.
C1.12 Engineering drawings
Engineering drawings are CAD produced drawings, which along with relevant CAM
programmes, could theoretically be used to manufacture the fully assembled car by a third
party. Such drawings must include all relevant dimensions, tolerances and material
information. STEM Racing™ engineering drawings must include detail to specifically identify
and prove compliance for the virtual cargo and wing surfaces. Engineering drawings can
include: orthographic projection, auxiliary projection, section views, isometric projection,
oblique projection, perspective and annotated renderings.
C1.13 Renderings
Renderings are images intended to illustrate the three-dimensional form of an object. These
can be generated in isometric projection, oblique projection or perspective.
C1.14 Team Digital Upload Folder
This is a team-specific digital upload folder, where all digitally submitted work must be
uploaded to STEM Racing™. Each team will receive a unique link to their own Team Digital
Upload Folder, which will be provided by email directly to competing teams and ICC’s after
team registration.
C1.15 Partnerships
A partnership can be defined as a collaborative relationship between organizations. The
purpose of this relationship is to work toward shared goals through a division of labour that all
parties agree on.

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 8 of 54 23 April 2025
ARTICLE C2 – GENERAL INFORMATION
C2.1 Competing teams
C2.1.1 STEM Racing™ will request that each In-Country Co-ordinator (ICC) selects teams
for entry to the World Finals event from their region. Once approved by STEM
Racing™, these teams will then be invited to compete in the World Finals by the
ICC. The invited World Finals teams will normally be the overall winner of the incountry national final, a second and third team chosen at the discretion of the ICC
to suit the In-Country competition. This third team could also be an internal or
international collaboration.
C2.1.2 Each team must consist of a minimum of 3 students to a maximum of 6.
If a student's date of birth falls after the 1st of January 2006 and they turned the age
of 19 in the year the event takes place, they are eligible to compete.
C2.1.3 Only members of the official competing team (maximum 6) are permitted to wear
the team’s uniform.
C2.1.4 STEM Racing™ will provide help to establish international collaboration teams
where needed by liaising between the relevant ICC’s. Teams nominated to form
international collaboration teams are usually runner-up or minor placed winning
teams from respective National Finals.
C2.1.5 International collaboration teams must consist of a minimum of 4 members and up
to a maximum of 6 with a minimum of 2 members from any one country (i.e. 3
countries collaborating is the maximum) and where possible be as balanced as
possible in order to represent a fair split of team members between the collaboration
countries.
C2.1.6 When teams combine to form a collaboration, a maximum of six students must be
nominated as the official competing team members. The remaining students may
be referred to as affiliated students. Regulation C2.2.3 does not apply to
International collaboration teams who have previously participated, provided the
same international collaboration team is not entered. (Please note, from 2015,
students who have previously attended a World Final as a collaboration team will
be allowed to compete a further time at a forthcoming World Final).
C2.1.7 During the competition, only the official core team members (maximum of 6) can
represent the team at registration, Pit Display set up, Scrutineering review, Verbal
Presentation, Design & Engineering judging, Project Management, Enterprise
judging, Safe/Fit to race fix, racing, on-stage presentations, competition activities
and any direct communication with the Chair of Judges or Event/Competition
Directors.
C2.1.8 If an international collaboration team wins an award, only the official core team
members may take to the stage and be involved in key photo, media and publicity
sessions. Any trophies must be shared between the team following the World Finals
event. Only the collaboration award will have two actual trophies associated with
it. Award certificates will be duplicated for awards won by collaboration teams.
C2.1.9 All international collaboration teams must sign a memorandum of understanding
(MOU) document that acknowledges the team construction, financial obligations
and team member responsibilities. This document must be signed by each team
member, a school official and the ICC as witness. This document should initially be
created by the ICC. Example MOU are available upon request from STEM
Racing™.
C2.1.10 Team affiliated students are welcome to attend the World Finals but must pay the
participation fee to join in all official activities. They may play no part in the judging
assessment process as outlined in C2.1.7. STEM Racing™ reserves the right to
impose a penalty of up to 20 points at the discretion of the chair of judges if it is felt
team affiliated students are influencing the judging process.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 9 of 54 23 April 2025
C2.1.11 Team affiliated students, supervising adults / teacher must adhere to C2.1.3. If a
uniform is to be worn it must be significantly different to the official core team. This
is to assist the Judges in recognising the official core students.
C2.1.12 Non-international collaboration teams may not have affiliated students associated
with the team and any additional delegates will only be recognised as team guests.
C2.2 Returning Students
C2.2.1 A student can only participate in a maximum of 2 World Finals.
C2.2.2 Any member of a World Finals Team (with the exception of C2.2.3), or the whole
team, may return to participate in one other World Finals event, provided they have
qualified to do so through their National Competition.
C2.2.3 After the 2018 World Finals, World Champions will not be able to compete in another
World Finals event. They may however be invited to join the Judging panel at a
future World Finals event.
C2.3 Competition programme, team number and team name
C2.3.1 STEM Racing™ will issue the competition programme showing all scheduled
judging activities, with judging times listed against team competition numbers.
C2.3.2 STEM Racing™ Ltd. will determine the team number each team will be allocated.
These team numbers will correspond with those published in the competition
programme.
C2.3.3 The competition programme may be revised slightly to accommodate a team from
the host country participating in the first race of the event.
C2.3.4 No teams participating in the challenge are permitted to use any of the Formula One
Word Marks (shown below) in their team name, logo, domain name, and/or any
social media handle. For example, “Infinity F1” is not allowed and should be
changed to something similar such as “Infinity” or “Team Infinity”. No team will be
permitted to use any of the prohibited word marks within their team name when
participating in STEM Racing™ from 2017 onwards.
The STEM RACING Logo, STEM RACING, FORMULA 1, FIA FORMULA ONE
WORLD CHAMPIONSHIP, GRAND PRIX and related marks are trademarks of
Formula One Licensing BV, a Formula 1 company. All rights reserved
C2.3.5 Duplicate team names will be asked to rename with the Country code after their
name. It is optional for teams to change their team logo, but all judging, references
and mentions will use the official corrected name.
C2.3.6 During registration teams will be asked to define their official team’s name and their
“short” team’s name. The official team’s name will be used to identify your team by
default. Please refer to C2.3.4 for guidance on creating a suitable team name.
The short name is the name that will be displayed for your team where space is
limited (for example, small on-screen graphics). This must be no more than 15
characters (including spaces) and be typed exactly as you want the name to appear.
C2.3.7 Prohibited characters – Teams may be asked to alter their team and organisation
names if they contain special characters outside of A-Z, a-z, 0-9 as these may cause
issues with data processing. Some of the reserved characters are listed below.
These may be amended at any point by STEM Racing™ Ltd. Superscript or
subscript characters will also be ignored.
• Team names must not include following reserved characters:
➢ < (less than)
➢ > (greater than)
➢ : (colon)
➢ " (double quote)
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 10 of 54 23 April 2025
➢ / (forward slash)
➢ \ (backslash)
➢ | (vertical bar or pipe)
➢ ? (question mark)
➢ * (asterisk)
C2.4 Team responsibilities
C2.4.1 Teams must read the World Finals Technical Regulations carefully to ensure their
cars comply with those regulations.
C2.4.2 Teams must read the World Finals Competition Regulations (this document)
carefully to ensure that all project elements satisfy these regulations and that they
understand the requirements and procedures for all aspects of the competition and
judging.
C2.4.3 During the competition it is the team’s responsibility to ensure that team members
are present at the correct time and location for all scheduled activities.
C2.5 Role and responsibility of ICC and supervising teacher/adult.
C2.5.1 All ICC’s and supervising teachers/adults should carefully read and understand the
terms and conditions for entry to the STEM Racing™ World Finals event, and must
have explained all relevant information within this agreement to their team/s.
C2.5.2 It is the primary responsibility of any event accredited supervising teacher/adult
and/or the ICC to ensure duty of care/well-being for all their student team members,
as appropriate for their home country legislation. Any concerns arising during the
event in relation to this should be brought to the attention of the STEM Racing™
Event Directors immediately.
C2.5.3 The event accredited supervising teacher/adult and/or ICC is expected to be present
during any judging activity with their team, but, must not interact in any way with the
student team, Judges or judging process. Any incident considered inappropriate will
be brought to the attention of the Chair of Judges and 10 penalty points may be
applied to their associated team.
C2.6 Regulations documents
C2.6.1 STEM Racing™ issues the regulations, their revisions and amendments made.
C2.6.2 Competition Regulations – (This document). The Competition Regulations
document is mainly concerned with regulations and procedures directly related to
judging and the competition event. Competition Regulation articles have ‘C’ prefix.
C2.6.3 Technical Regulations – A document; separate to this one which is mainly
concerned with those regulations that are directly related to STEM Racing™ car
design and manufacture. Technical Regulation articles have a ‘T’ prefix.
C2.7 Interpretation of the regulations
C2.7.1 The final text of these regulations is in English, should any dispute arise over their
interpretation, the regulation text, diagrams and any related definitions should be
considered together for the purpose of interpretation.
C2.7.2 Text clarification - Any frequently asked questions that are deemed by STEM
Racing™ to be related to text needing clarification will be answered. The question
and the clarification will be published to all teams at the same time.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 11 of 54 23 April 2025
C2.8 Supplementary competition regulations
Other documents may be issued by STEM Racing™ that provide teams with further logistic
and other important event information. Any supplementary regulations will be issued to all
ICC’s or lead teachers and team managers, where the team manager has supplied STEM
Racing™ with a contact email address. Copies of all supplementary regulations issued will be
available online either via the website, event app or social media pages.
C2.9 Design ideas and regulation compliance queries
Teams are not permitted to seek a ruling from STEM Racing™ or any competition official or
judge before the event as to whether a design idea complies with the regulations. Rulings will
only be made by the Judges at the World Finals event. Design compliance to the regulations
forms part of the competition. As in Formula 1®, innovation is encouraged, and STEM
Racing™ teams may also find, sometimes controversial, ways of creating design features by
pushing the boundaries in order to get an extra competitive edge.
C2.10 Team partnerships
C2.10.1 STEM Racing™ teams are encouraged to develop mentoring partnerships with
businesses, industry, or higher education organisations throughout their project.
C2.10.2 All teams will be required to complete a ‘Team Partnerships’ declaration using the
template issued by STEM Racing™. A declaration is required even in the case of
no partnerships to declare. This is submitted as per Article C2.13.
C2.10.3 All design work, text and scripting for all project elements presented for assessment
must be wholly undertaken and created by the team. This includes all CAD and CAM
data, electronic portfolio and graphic content.
C2.10.4 All aspects of any partnerships should also be represented in the team’s portfolio.
For project elements produced utilising some outside assistance, teams should be
able to demonstrate to the Judges a high level of understanding of, and justification
for, any of the processes used.
C2.10.5 ‘Common sense’ will prevail for project elements or components that a team has
purchased from a supplier. E.g. bearings, screw eye, display hardware. Teams
should be able to explain and justify why a specific component was selected /
purchased over other similar available components.
C2.11 Mandatory project elements required for World Finals entry
Following is a summary of the mandatory elements required for judging:
• Two (2) identical STEM Racing™ cars including all optional replacement components
• One (1) STEM Racing™ display car for use in judging activities
• One (1) fully machined, unfinished, unassembled STEM RACING model block car
body identical to the car body used on car A & B
• One (1) Halo and One (1) Helmet identical to the car body used on car A & B (for
specification judging purposes)
• One (1) digital and Two (2) physical copies of the Design & Engineering Portfolio
• One (1) digital and Two (2) physical copies of the Project Management Portfolio
• One (1) digital and Two (2) physical copies of Enterprise Portfolio
• A Pit Display
• A 10-minute Verbal Presentation
• A set of engineering drawings including orthographic and 3D renders for
Scrutineering judging.
• A digital team logo
• All relevant CAD data and access to CAD software
• ‘Team Partnerships’ declaration(s)
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 12 of 54 23 April 2025
• Car Submission Checklist which must include the official STEM RACING Model
Block holographic stickers
The above list is detailed in the remainder of ARTICLE C2.
C2.11.1 Cars - Each team must produce two (2) identical STEM Racing™ race cars and one
(1) display car.
C2.11.2 Portfolios - Each team must produce:
• One (1) digital and Two (2) physical copies A3, 11-page (maximum) Design &
Engineering portfolio
• One (1) digital and Two (2) physical copies A3, 12-page (maximum) Enterprise
portfolio
• One (1) digital and Two (2) physical copies A3, 7-page (maximum) Project
Management portfolio
Portfolios must be presented in an A3 (or equivalent) sized format. Refer to
ARTICLE, C5, C6 & C7 of these regulations along with the Design & Engineering,
Project Management and Enterprise judging scorecards for portfolio requirements.
Teams must submit their portfolio documents (Design & Engineering, Project
Management, Enterprise) in digital format to the STEM Racing™ World Finals
before Sunday 14th September 2025 23:00 (GMT/UTC +00:00). Late
submissions will incur a 20-point penalty. Submissions must be via Team Digital
Upload Folder. (Refer ARTICLE C1.14)
If you have any issues uploading your documents, you can also submit them by
email to stemracinghq@gmail.com. It is recommended that when creating PDF
files, teams consider embedding any unusual font types they may have used
within their documents to help ensure they display correctly when opened by the
Judges.
The following file conventions must be adhered to:
▪ Documents must be submitted in separate single Portable Document Format
(PDF) files.
▪ PDF files must be no greater than 20Mb in size for the email option and no
greater than 75MB for the STEM Racing™ upload folder option.
▪ Text included in the PDF files must be highlightable to facilitate the similarity
checking process. STEM Racing™ reserves the right to impose a penalty of
up to 20 points to any team failing to comply with this request at the discretion
of the chair of judges.
The files must be named:
“teamnumber_team_name_country_engineering.pdf”,
“teamnumber_team_name_country_projectmanagement.pdf”
“teamnumber_team_name_country_enterprise.pdf”
“teamnumber_team_name_country_engineering_drawings_renders.pdf”
so they can be recognised easily when submitted.
For example: “T01_STEM_RACING_UK_projectmanagement.pdf”.
C2.11.3 Pit display - Each team will be provided with a dedicated exhibition style space for
set-up of their pit display elements. The specific style and size of this space will be
announced in supplementary event competition regulations. Refer to ARTICLE C7
for further pit display specifications and content requirements.
C2.11.4 Verbal Presentation - Teams will be required to deliver a Verbal Presentation in
relation to their project to the Judges. The presentation must not last longer than 10
minutes. If teams are unable to deliver the presentation in English, then an
interpreter can be present (teams need to bring their own translator) and a time of
20 minutes will be allocated, but the team must notify us if this is the case no later
than Monday, 25
st August 2025. Teams should bring their own laptop with any slide
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 13 of 54 23 April 2025
show or other multimedia files that need to be shown as part of their Verbal
Presentation. Any team who needs a laptop for Verbal Presentation judging and is
unable to bring one to the World Finals must contact STEM Racing™, (globaladmin@stemracing.com), at least one month before the event. Refer to ARTICLE
C7 of these regulations for details regarding presentation content and other
requirements.
C2.11.5 Electronic data - Teams must submit all additional project data as specified below:
Data submitted must include:
All CAD parts and assembly files to assist the scrutineering process.
The files must be named: “teamnumber_team_name_country_filename”, so
they can be recognised easily when submitted. For example:
“T01_STEM_RACING_UK_full_car_assembly.stl”.
Teams must submit their files to STEM Racing™ before Sunday, 14th September
2025 23:00 (GMT/UTC +00:00). Late submissions will incur a 20-point penalty.
Submissions must be via Team Digital Upload Folder. (Refer ARTICLE C1.14)
This data may be referred to for judging purposes and possible marketing and
promotion following the event.
C2.11.6 Engineering Drawings (refer to ARTICLE C1.12) and Renderings (refer to ARTICLE
C1.13) for Specification Judging. Teams must submit both a digital copy and a hard
copy of any engineering drawings and renderings of their car assembly and parts
they wish to be referenced by the Engineering and Specification Judges. The digital
submission must exactly match the hard copy in content and format.
Each team must produce:
• One (1) hard copy of A4 Engineering drawings including orthographic view
• One (1) hard copy of A4 3D car renders
• One (1) digital copy of A4 Engineering drawings including orthographic view
• One (1) digital copy of A4 3D car renders
Mandatory table of contents for Engineering Drawings
Teams MUST include the following Engineering Drawing Table of Contents
1. Orthographic drawings with detailed dimensions of fully assembled car indicating
regulation compliance
2. Exploded isometric drawing with key to main components
a. Car body
b. Virtual cargo
c. Chamber
d. Tether line guides
e. Front wheels / wheel support system
f. Rear wheels / Wheel support system
g. Nose cone
h. Front wing / support structure
i. Rear wing / support structure
3. Orthographic drawings with detailed dimensions of virtual cargo including a sectioned
view.
4. Location of official STEM Racing™ decals dimensioned from key structural parts (eg
wheel centre).
5. Chamber details including wall thickness and depth.
6. Orthographic drawings with detailed dimensions of tether line guides.
7. Orthographic drawings of wheels with sectioned view and detailed dimensions.
8. Orthographic drawings with detailed dimensions of front wheels / wheel support
system.
9. Orthographic drawings with detailed dimensions of rear wheels / wheel support
system.
10. Orthographic drawings with detailed dimensions of nose cone.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 14 of 54 23 April 2025
11. Orthographic drawings with detailed dimensions of front wing and support structure
highlighting wing surface/boundary.
12. Orthographic drawings with detailed dimensions of rear wing and support structure
highlighting wing surface/boundary.
13. Detailed description of intended quality and finish in relation to individual components
/ assembled car.
Hard copy requirements:
The drawing set must include an Orthographic Drawing - A 1
st or 3
rd angle orthographic
projection, including plan, side and end elevations of the fully assembled car. 3D rendering/s
of the final car design must also be included. These elements must be produced using CAD.
The orthographic technical drawing should include dimensions and corresponding regulation
numbers to illustrate regulation compliance. These drawings must be presented on paper only
pages no larger than A4 in size. Please note, Engineering Drawings and Renderings will be
stored along with your car and spare parts after Registration and Element Submission, so hard
covers and / or large bindings are not advisable. Paper versions of the Engineering Drawings
and Renderings are to be submitted with the team’s cars (Refer ARTICLE C2.13.1).
Digital copy requirements:
Teams must submit their A4 Engineering Drawings and Renderings in digital
format to the STEM Racing™ World Finals before Sunday 14th September 2025
23:00 (GMT/UTC +00:00). Late submissions will incur a 20-point penalty.
Submissions must be via Team Digital Upload Folder. (Refer ARTICLE C1.14)
C2.11.7 Computer for Design & Engineering judging - a computer with the CAD software
used by the team and with all CAD parts and assembly data should be used during
the Design & Engineering judging session so that the team can demonstrate their
CAD work and better explain how they engineered their car design.
C2.11.8 ‘Team Partnerships’ declaration – Every team must complete the declaration
template online as issued by STEM Racing™. All partnerships and any outside
assistance must be included. This document will be referenced by Judges so they
can better understand team partnerships and ask questions, and therefore must
be a full and accurate declaration.
Please complete the partnership declaration here.

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 15 of 54 23 April 2025
C2.12 Team registration
C2.12.1 Teams are required to register with STEM Racing™ at the event. At this
registration, teams will be issued with World Finals accreditation, event
programmes and detailed welcome pack. The team manager and supervising
adult for each team must attend and submit their project elements. Each team
must submit their flight details by Friday 5
th of September 2025. Each team will
then be given a specific time and location to register prior to their arrival at the
venue, this time slot must be adhered to.
Registration will close at 18:00 local time on the designated registration day.
STEM Racing™ reserves the right to impose a penalty of up to 50 points to
any team arriving late at the discretion of the Chair of Judges.
STEM Racing™ advises that teams plan their travel to arrive at least 3 hours
before registration officially closes.
C2.12.2 Official STEM Racing™ 30x15mm car decals will be provided for teams that have
not manufactured their own. These decals must be fitted to each of the two
submitted cars by the STEM Racing™ team during Specification judging. You can
download the decal artwork here.
C2.13 Submission of project elements
C2.13.1 A time and location will be published in the event programme for when each team
must submit their project elements. This will occur well before judging commences.
Following is a list of the elements which must be submitted by each team at this
time:
PHYSICAL PROJECT ELEMENTS
• One (1) nominated Car A identified using a white or black background
STEM Racing™ ‘Car A’ logo decal
• One (1) nominated Car B identified using a white or black background
STEM Racing™ ‘Car B’ logo decal
• One (1) fully machined, unfinished, unassembled STEM RACING model
block car body identical to the car body used on car A & B
• One (1) Halo and One (1) Helmet identical to the car body used on car A &
B (for specification judging purposes)
• Optional Replacement Components
▪ Nose cone & front wing assembly – maximum of two (2)
▪ Rear wing assembly – maximum of two (2)
▪ Front wheels – maximum of four (4)
▪ Front wheel support structure – maximum of two (2)
▪ Rear wheels – maximum of four (4)
▪ Rear wheel support structure – maximum of two (2)
• One (1) set of A4 Engineering drawings (with mandatory table of
contents)
• One (1) set of A4 Car renders for Scrutineering judging
• Two (2) physical copies of the Design & Engineering Portfolio
• Two (2) physical copies of the Project Management Portfolio
• Two (2) physical copies of Enterprise Portfolio
• Project Elements Submission Checklist, which must include the official
STEM RACING Model Block holographic sticker.
DIGITAL PROJECT ELEMENTS
• 1 x digital A3, 11-page (1-page front cover + 10 pages of content) Design
& Engineering Portfolio
• 1 x digital A3, 12-page (1-page front cover + 10 pages of content + 1 page
back cover) Enterprise Portfolio
• 1 x digital A3, 7-page (1-page front cover + 6 pages of content) Project
Management Portfolio
• Digital A4 Engineering drawings (with mandatory table of contents)
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 16 of 54 23 April 2025
• Digital A4 Car renders for Scrutineering judging
• Electronic copy of all additional project data
• ‘Team Partnerships’ declaration(s) must be completed online prior to the
event.
All digital project elements must be digitally submitted before Sunday 14th September
2025 23:00 (GMT/UTC +00:00). Refer to ARTICLE C2.11.
C2.13.2 During project submission, each team will be given the opportunity to check the
weight of their cars on the official World Finals scales. If either car being submitted
is under the minimum weight, the team will be permitted 15 minutes to fix any issue
so that both cars can be submitted at or above the minimum weight.
C2.13.3 Small coloured ‘dot’ stickers (approximately 5mm in diameter) and supplied by
STEM Racing™, will be adhered to the underside of each car. The stickers will
feature the team’s competition number.
C2.13.4 Once cars and replacement components have been submitted, they are considered
as being in parc fermé.
C2.14 Project elements to be retained by STEM Racing™
It is a condition of World Finals entry that each team permits STEM Racing™ to retain one (1)
car, one of each physical portfolio (Design & Engineering, Project Management, Enterprise)
and the electronic copy of all specified project data submitted. Teams also permit STEM
Racing™ to use any of these project elements for marketing purposes and/or publication as
exemplar projects for reference by others.
C2.15 Benefit of doubt
The Chair of Judges will, where appropriate, seek to use ‘benefit of doubt’ when the
assessment of compliance is marginal or unclear. In this situation, teams will be given the
benefit of doubt rather than a firm penalty if a penalty cannot be clearly measured or identified.
C2.16 Spirit of the competition
Teams are expected to act in the spirit of the competition, both before and during the STEM
Racing™ World Finals. Any team deemed by the Chair of Judges to be acting outside of the
spirit of the competition, can be removed from certain or all aspects of the competition. For
example, a team attempting to abuse the technical regulations to their advantage may, at the
discretion of the Chair of Judges, be removed from racing and receive no points for this
activity. A team deemed to be acting in an unsportsmanlike manner towards another team or
other persons may be removed from some or all judging areas.
The spirit of the competition is simple; embrace and respect the rules and regulations, do your
very best to compete legally and fairly, while contributing positively to the STEM Racing™
World Finals. Make friends, create positive relationships, network professionally and enjoy
yourselves.
C2.17 Plagiarism
Plagiarism within any project work submitted by teams is not permitted. All teams must
complete the Originality Declaration as part of their online team registration. Where
plagiarism has been detected, the Chair of Judges may choose to penalise or exclude the
team from that element of the competition.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 17 of 54 23 April 2025
ARTICLE C3 – COMPETITION AND JUDGING FORMAT
C3.1 Competition programme
C3.1.1 Each team will be judged as per the competition programme. The competition
programme will be formulated by STEM Racing™ to best and fairly accommodate
all judging and other competition activities. Teams will rotate around judging
activities as per this programme, with each rotation usually of 30 minutes in duration.
C3.1.2 Judging Streams – The competition programme will normally be divided into multiple
parallel judging streams (Stream A, Stream B, Stream C and Stream D), to help
ensure quality judging time intervals within the event time constraints. A number of
strategies are implemented within the judging process, including judge briefings and
judge reviews for cross-moderation to ensure there is consistency across the
judging streams.
C3.2 Judging categories
There are six (6) main judging categories, each with its own team of Judges/officials and
specified judging activities as detailed in further articles.
• Specification & Scrutineering Judging
• Design & Engineering Judging
• Project Management Judging
• Enterprise Judging
• Verbal Presentation Judging
• Racing
C3.3 Judging scorecards
The STEM Racing™ World Finals judging scorecards provide detailed information in relation
to what the Judges will be looking for. They include key performance indicators, which are
referred to by the Judges in awarding points during judging activities. The 2025 World Finals
judging scorecards can be found in the appendix of this document. Please read the whole
document without assumptions from previous rules documents.
READING THE SCORECARDS CAREFULLY IS IMPORTANT. THEY PROVIDE CRITICAL
INFORMATION FOR TEAMS AS TO WHAT NEEDS TO BE PRESENTED FOR EACH
JUDGING CATEGORY.
C3.4 World Champions
The STEM Racing™ World Champions perpetual trophy will be awarded to the team with the
highest sum total from all judging categories (ARTICLE C3.5). In the case of a tied points
score, the team with the highest time trial score will be determined the winner.
THE CHAIR OF JUDGE’S DECISION IS FINAL
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 18 of 54 23 April 2025
C3.5 Point allocations
Points will be awarded to teams across six (6) categories with maximum possible scores as
detailed in the following table:
World Finals Judging Categories and Point Allocations
Specification & Scrutineering Judging
Specifications 100 points
Engineering Drawings 20 points
3D Renders 20 points
Quality of Finish and Assembly 20 points
Design & Engineering Judging
Design & Engineering Portfolio 180 points
Project Management Judging
Initiating 35 points
Planning 25 points
Executing 20 points
Monitor and Controlling 10 points
Enterprise Judging
Enterprise Portfolio Only Assessment 100 points
Team Identity 20 points
Pit Display 60 points
Verbal Presentation Judging
Technique 60 points
Composition 40 points
Subject Matter 40 points
Racing
Time Trials 105 points
Reaction Racing 105 points
Knock-Out Racing 30 points
Fastest Car Bonus 10 points
TOTAL 1000 points
The International Rules Committee may at their discretion add point scoring judging categories into
the event. This would be completed under controlled conditions during the competition.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 19 of 54 23 April 2025
C3.6 Classification of technical regulations
C3.6.1 The technical regulations are classified as either: GENERAL, SAFETY, PERFORMANCE.
GENERAL SAFETY PERFORMANCE
Regulations that shape the
way the car fundamentally
looks and works, vital to the
style of a STEM Racing™ car.
Mandatory rules that govern the
safe running of the car. Cars
must meet these rules to be
considered ‘safe to race’.
Rules that have a direct impact
on the performance of the
vehicle, these typically carry the
heaviest penalties.
C3.6.2 If a race car is judged as being NON-COMPLIANT with any Performance regulation
they will be INELIGIBLE for the awards of: ‘Fastest Car’ and ‘Best Engineered
Car’.
If a race car is judged as being NON-COMPLIANT with any Performance regulation,
racing leaderboards will show an “under investigation” symbol next to the team’s
race time.
For the Knock-out Competition, should there be any teams with Performance
regulation failure(s) for both cars seeded in the top 24 teams then they will only be
permitted to race in round one of the knock-out competition and will be automatically
knocked out during round one regardless of the race result.
All Performance regulations are highlighted in yellow throughout the Technical
Regulations Document:
T3.3, T3.6, T4.2, T4.4.1, T5.6, T7.2, T7.3, T7.4, T7.5, T7.6, T7.7, T7.8, T7.9, T7.10,
T7.11, T8.6.1, T8.6.2, T8.6.3, T8.7, T8.8, T9.5.1, T9.5.2, T9.5.3, T9.6, T9.7.
For more information regarding Compliance with regulations, please consult T2.5 of
the Technical Regulations document.

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 20 of 54 23 April 2025
ARTICLE C4 – SPECIFICATION & SCRUTINEERING JUDGING (160 points)
C4.1 What will be judged?
Specification & Scrutineering judging is a detailed inspection process where BOTH race cars
plus the optional replacement components are assessed for compliance with the STEM
Racing™ World Finals Technical Regulations. The Engineering drawings, renderings and
quality of finish & assembly will also be assessed. Refer to the scrutineering and specification
judging scorecards for scoring details.
C4.1.1 Optional replacement components must be identical in design to those fitted to both
cars (Car A & Car B) and must be submitted with the cars. Only the following
replacement components are permitted:
o Nose cone & front wing assembly – maximum of two (2)
o Rear wing assembly – maximum of two (2)
o Front wheels – maximum of four (4)
o Front wheel support structure – maximum of two (2)
o Rear wheels – maximum of four (4)
o Rear wheel support structure – maximum of two (2)
o Halo & Helmet – maximum of two (2)
Submitted replacement components that are determined by the Judges to not be
identical to that which are fitted to the car will not be allowed to be used. Submitted
components will remain in parc fermé and only be handed back to the team if
needed during racing and/or car servicing.
C4.2 Team preparation
Teams must ensure that their cars (Car A & Car B) and any optional replacement components
are complete and ready for specification judging and racing before they are submitted. Notice
is also drawn to the performance regulations, refer ARTICLE C3.6. Teams must have also
submitted an electronic copy of all specified project data such as scrutineering engineering
drawings, which may all be referenced. Refer ARTICLE C2.11
C4.3 Who needs to attend?
This inspection will take place live in the presence of the team (represented by up to 2 team
members and 1 supervising adult). Teams will proceed through stations where STEM Racing
judges will verify all dimensions and specifications. Each station visit will last approximately
10 minutes, during which scrutineers will review the cars' elements for compliance with the
2025 Technical Regulations.
C4.4 Judging process/procedure
Teams begin specification judging with a full allocation of 100 points. Any infringements of the
Technical Regulation articles, on either car, will result in points being deducted as detailed in
the Technical Regulations.
THE PROCESS
1. Before the measuring process begins, STEM Racing will create a photographic record
of both of your race cars.
2. The designated team members may observe the measuring process, but they are not
permitted to intervene.
3. If the judges detect a compliance issue with a specific regulation, the team will be
informed.
4. Teams may ask questions, provided they do not interfere or cause delays within the
station's allocated time.
5. Each judging station will have two judges present. Scrutineering supervisors,
including the Head of Scrutineering and the Chair of Judges, will oversee this process.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 21 of 54 23 April 2025
6. At the conclusion of the specification process, teams will have an opportunity to
appeal any judge’s decision. Please see ARTICLE C11 – PROTESTS.
7. Teams flagged for performance-related regulation issues will be marked on the racing
leaderboards with an “under investigation” symbol.
In addition, the engineering drawings, renderings, and overall quality of finish and assembly
will be assessed, though this evaluation will occur behind closed doors. Refer to the
scrutineering and specification judging scorecards for detailed scoring criteria.
CONTINUAL ASSESSMENT
Spot checks of the cars may take place at any point during the competition. STEM Racing
reserves the right to review specification results if necessary. Teams will be informed of any
changes to the initial assessment, and an appeal window may be made available at the
discretion of the Chair of Judges.
C4.5 Safe/Fit to race fix
Teams that have been judged during initial scrutineering to have incurred a Safe/Fit to Race
regulation from the list below will be provided with a special 20-minute car service time, prior
to the commencement of racing. Cars must meet these rules to be considered ‘Safe/Fit to
race. If during this service time the car can be modified so as to comply with the failed
regulation(s), the team will then only incur HALF the point’s penalty for that infringement,
without being classified as having incurred a SAFETY infringement.
T3.2 T4.4.4, T4.4.5, T5.1, T5.3, T5.4, T5.5, T5.6, T6.1, T6.2, T6.3 and T7.13
C4.6 Specification judging decision appeals
C4.6.1 Scrutineering Decision Appeals
These must be submitted within two hours of the team completing their
specification review judging. Other rules for submitting these will be the same as
for protests.
C4.6.2 Submitting a Protest
Any protest issues must only be submitted by the team manager by email (globaladmin@stemracing.com) to an Event Director, who will register this and
immediately submit it to the Chair of Judges. This must occur no later than 21:00
(local time) on racing day 2. Any protest or appeals submitted after this time may
be disregarded. The Chair of Judges decision related to any protest is final.
Teams should carefully consider their grounds for submitting a protest or appeal.
Any protest or appeal that is unsuccessful, with the Judges initial decision
remaining unchanged, will result in the team having a 15-point penalty applied
against their total score.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 22 of 54 23 April 2025
ARTICLE C5 – DESIGN & ENGINEERING JUDGING (180 points)
C5.1 What will be judged?
The Design & Engineering Judges will examine each team’s 11-page Design & Engineering
portfolio so that they can assess the teams' car design and use of CAD/CAM technologies
along with the quality of manufacture of both race cars submitted. The specific areas to be
assessed are:
o Design Concepts
o CAD 3D Modelling
o Application of Computer Aided Analysis
o Use of CAM/CNC
o Other Manufacturing & Assembly
o Research & Development
o Testing
o Design Process Evaluation
o Document Presentation
Refer to the Design & Engineering judging scorecard for key performance indicator
information.
C5.2 Team preparation
A laptop needs to be ready and taken to the Design & Engineering judging team along with
any other items which may help the team explain any engineering or manufacturing concepts.
The Design & Engineering Judges will not have access to the team pit display for judging
purposes. Teams may choose to, but do not need to take their display (3rd) car to the Design
& Engineering judging. Preparation should include careful reading of the scorecard. The key
performance indicators for the design process, application of CAD / CAM, analysis and
associated data organisation, describe what the Judges will be looking for.
C5.3 Who needs to attend?
This judging session must be attended by the team manager and team design and
manufacturing engineers as a minimum.
C5.4 Judging process / procedure
Teams will be awarded points as per the key performance indicators shown on the Design &
Engineering scorecard. Judges will review the Design & Engineering portfolio in a ‘closed to
teams’ session programmed before the commencement of scheduled judging sessions. The
scheduled Design & Engineering judging interview session will focus on the overall
engineering and design of the car. This is an informal interview where Judges will ask the
team to demonstrate their CAD / CAM work and query teams on what they have done. The
quality of car manufacture and car assembly will be judged during a separate ‘closed to teams’
session.
An interpreter can be present during the judging session (teams need to bring their own
translator) but no extra time will be added.
C5.5 Design & Engineering Portfolio requirements
The Design & Engineering portfolio must be in a digital and printed format of A3 or similar
size. The portfolio is limited to 11 pages (1-page front cover + 10 pages of content). This can
be a single page front cover plus 10 single sided or 5 double sided sheets. If a portfolio
comprises more than 11 pages, the Judges will only review the first 11 pages for assessment
purposes. There MUST be content related to the use of CAM and CNC manufacturing
included in the portfolio and this will be referenced by the Engineering Judges. Content related
to the car, design ideas, design development, research, testing and evaluation should be
presented within the portfolio.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 23 of 54 23 April 2025
ARTICLE C6 – PROJECT MANAGEMENT JUDGING (90 points)
C6.1 What will be judged?
The Project Management judges will examine each team’s 7-page Project Management
Portfolio so that they can assess the following specific areas.
Project Management:
• Initiating
o Initiation Process
o Project schedule
• Planning
o Budget & Resource management
o Roles and Responsibilities
• Executing
o Team & Stakeholder Communications
o Risk Management
• Monitor and Controlling
o Monitoring & Controlling
Refer to the Project Management scorecard for detailed point scoring and key performance
indicator information.
C6.2 Team preparation
Each team must prepare one (1) Project Management portfolio as per ARTICLE C2.11. Most
importantly, teams need to read the Project Management judging scorecard carefully to
ensure that all areas to be assessed are included within the context of their Project
Management portfolio.
C6.3 Who needs to attend?
All team members must be present during the Project Management judging session.
C6.4 Judging process / procedure
The Project Management judging will take place during dedicated judging session. Team
members may be asked questions by Judges to help them find certain content and/or seek
further explanation. In addition to the scheduled judging session, the Judges will also be given
time to conduct pre-judging and review of each team Project Management portfolio. This will
be a ‘closed to teams’ session programmed before the commencement of scheduled judging
sessions.
An interpreter can be present during the judging session (teams need to bring their own
translator) but no extra time will be added.
C6.5 Project Management Portfolio requirements
The Project Management Portfolio must be in a digital and printed format of A3 or similar
size. The Project Management portfolio is limited to 7 pages (1-page front cover + 6
pages of content). This can be a single page front cover plus 6 single sided or 3 double
sided sheets. If the portfolio comprises more than 7 pages, the Judges will only review the
first 7 pages for assessment purposes.
For Project Management, teams are asked to detail their project management processes
employed with the delivery of the STEM Racing™ Project. The STEM Racing™ Project
Management Guide should be used for reference. You can find the guide here.
The number of pages allocated to each key performance indicators is at the discretion of
each team.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 24 of 54 23 April 2025
ARTICLE C7 – ENTERPRISE JUDGING (180 points)
C7.1 What will be judged?
The Enterprise Judges will examine each team 12-page Enterprise Portfolio and Pit Display
so that they can assess the following specific areas.
• Enterprise Portfolio only assessment:
o Marketing Strategy & Materials
o Sponsorship & Return on Investment
o Digital Media Proficiency
o Sustainability
o Document Presentation
• Pit Display
o Design Process (Documented in Enterprise Portfolio)
o Content, Clarity, and Impact
o Functionality & User Experience execution
• Team Identity
o Overall Team Identity
The Pit Display Criteria (Design Process, Content, Clarity and Impact and Functionality & user
experience) will primarily be based on the Pit display, Pit display designs, enterprise portfolio
and the interviews with the Enterprise judges.
The Overall Team Identity will be assessed based by looking at all aspects of the team’s
identity. This will be primarily based on the Pit display, enterprise portfolio and the interviews
with the Enterprise judges. Judges may also review other documentation, such as the
engineering and project management portfolios and images of the car to confirm the team’s
identity has been applied consistently.
Refer to the Enterprise scorecard for detailed point scoring and key performance indicator
information.
C7.2 Team preparation
Each team must prepare one (1) Enterprise Portfolio and Pit Display as per ARTICLE
C2.11. Most importantly, teams need to read the Enterprise judging scorecard carefully to
ensure that all areas to be assessed are included within the context of their Enterprise
portfolio and Pit Display.
It is each team’s decision how and where each area is presented. Teams should be mindful
of the time constraints of judging when making these decisions.
C7.3 Who needs to attend?
All team members must be present during the portfolio and display judging session.
C7.4 Judging process / procedure
The Enterprise judging will take place during dedicated judging session. Team members may
be asked questions by Judges to help them find certain content and/or seek further
explanation. In addition to the scheduled judging session, the Judges will also be given time
to conduct pre-judging and review of each teams Enterprise Portfolio and Pit Display. This will
be a ‘closed to teams’ session programmed before the commencement of scheduled judging
sessions. An interpreter can be present during the judging session (teams need to bring their
own translator) but no extra time will be added.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 25 of 54 23 April 2025
C7.5 Enterprise Portfolio requirements
The Enterprise Portfolios must be in a digital and printed format of A3 or similar size.
The Enterprise portfolio is limited to 12 pages (1-page front cover + 10 pages of content +
1 page back cover). This can be a single page front cover plus 10 single sided or 5 double
sided sheets and a single page back cover. If the portfolio comprises more than 12 pages,
the Judges will only review the first 11 pages for assessment purposes. The back cover of
the portfolio should include the STEM Racing™ logo, the team logo and a team photo.
o Marketing Strategy & Materials
For the marketing element, teams are asked to summarise their approach and
reasoning to gaining awareness via marketing activities.
o Sponsorship & Return on Investment (ROI)
For this element, teams are asked to explain their engagement with sponsors,
explaining the relationship and benefits. Teams should also explain their activities
linked to return of investment.
o Digital Media Proficiency
For this element, teams are asked to outline their approach and reasoning for social
media platforms, electronic mailings, website, and other online communications. The
Digital Media element within the document will be assessed in conjunction with a review
of the team’s Digital Media campaign executed.
o Sustainability
For this criterion, teams are to outline their sustainability strategy and activities which
give consideration to economic, environmental, and social factors.
The number of pages allocated to each key performance indicators is at the discretion of each
team.
C7.6 Pit Display setup and parameters
C7.6.1 The Team Pit Display is at the heart of a STEM Racing™ event. It is the base of a
team and says everything about a Team’s identity, USP (Unique Selling Point),
brand and design development journey. STEM Racing™ will provide each team with
a self-contained exhibition style display space including integrated lighting and 1 x
power supply with pins and rating configured to the host country format. Teams need
to supply any power adaptors they may require. Display spaces are normally of
approximate dimensions 3m wide x 1m deep x 2.4m high. The precise space
description and dimensions will be announced closer to the event
C7.6.2 A time period will be scheduled for when all teams will set-up their Pit Displays. A
time limit of two hours will be enforced; this will be confirmed in supplementary
regulations. STEM Racing™ reserves the right to apply a penalty of up to 20 points
at the discretion of the Chair of Judges for teams that do not complete their set-up
within the time limit, do not leave their stand in a safe state and clear their pit and
surrounding area of all rubbish.
C7.6.3 No part of the teams completed Pit Display is allowed to protrude beyond the
physical dimensions of their allocated pit space. This includes anything that might
protrude above the pit space highest point e.g. flags. Teams are not permitted to
remove any part of the provided exhibition booth to fit the pit display. A penalty of
up to 10 points may be applied at the chair of judge’s discretion.
C7.6.4 ONLY student team members are permitted to set-up their pit displays. There must
be no supervising teacher / adult or other outside assistance, unless deemed by
STEM Racing™ to be a health and safety issue. A penalty of up to 20 points may
be applied at the Chair of Judge’s discretion.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 26 of 54 23 April 2025
C7.6.5 STEM Racing™ and/or the Chair of Judges may instruct a team to take action to
reduce noise or remove display inclusions deemed to be inappropriate. STEM
Racing™ will instruct teams to remove or alter any display inclusions considered to
be a safety hazard.
C7.6.6 Any electrical appliance connected to the power supply must be safe and compatible
with the host country power rating.
C7.6.7 The pit display should be designed in such a way as that it can be dismantled and
rebuilt in a different location during or after the event. This is to allow pit displays to
be rebuilt for promotional purposes in strategic locations over the Grand Prix
weekend.
C7.6.8 As part of our sustainability objectives, teams will no longer be able to send pit
displays as freight to any future World Finals including the 2025 event. If your team
attempts to freight anything to the venue, we will refuse delivery.
C7.6.9 All pit display materials must be “hand carried”, by the team, into the World Finals
event venue. Cases with wheels to be rolled in are allowed. We recommend that the
dimensions would be acceptable by an airline for checked baggage into the hold of
an aircraft. All materials brought into the venue must be taken away at the end of
the event. Production companies will not be allowed to assist teams on the
transportation or assembly of pit displays.
STEM Racing™ recommends no item should weigh more than 30kg and total length
+ height + depth of any item should not exceed 240cm.
Pit display set up – Team Abiyya from Saudi Arabia – Aramco STEM Racing™ World Finals 2023
C7.6.10 There will be no waste (rubbish) disposal options during pit build and breakdown.
Your pit display area must be left as you found it.
IMPORTANT HEALTH & SAFETY: The Health and Safety of yourselves and those
around you must be considered when working on all aspects of your Pit Display to
ensure a safe environment for everyone. STEM Racing™ expects teams to produce
a risk assessment and method statement to ensure all team members are aware of
any risks in the construction of the pit display. Displays must be safe for other
participants and visitors to the event. STEM Racing™ reserves the right to apply a
penalty of up to 20 points at the discretion of the Chair of Judges for unsafe activity
and any unsafe elements of the pit display may be removed.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 27 of 54 23 April 2025
ARTICLE C8 – VERBAL PRESENTATION JUDGING (140 points)
C8.1 What will be judged?
The Verbal Presentation Judges will assess each teams’ 10-minute Verbal Presentation
across the areas of technique, composition and subject matter:
• Technique
o Engagement & Presentation Dynamics
o Team Contribution
• Composition
o Content Quality, Relevance & Subject Understanding
o Time, Clarity and structure of content
• Subject
o Innovation – detail key innovations related to car design, project management,
marketing or any other aspect of the team’s project
o Collaboration – detail any partnerships or mentoring from outside the team
and justify in terms of improving project outcomes
o STEM Racing™ learning journey
Refer to the Verbal Presentation judging scorecard for detailed point scoring and key
performance indicator information.
C8.2 Team preparation
Each team is required to prepare a Verbal Presentation as per the requirements at ARTICLE
C2.11. Teams need to have all presentation resources tested and ready with them for Verbal
Presentation judging. Most importantly, teams should read the Verbal Presentation judging
scorecard carefully to ensure their Verbal Presentation features all elements and content that
the Verbal Presentation Judges will be looking for.
C8.3 Who needs to attend?
All team members must be present during the Verbal Presentation judging session.
C8.4 Judging process / procedure
Verbal Presentation judging is scheduled for the same duration of other judging sessions,
usually 30 minutes. Teams will be given an opportunity at the start of their time to set-up and
test their laptop and any other presentation technologies and resources. The team will inform
the Judges when they are ready to begin. The Judges start timing the 10 minute duration (20
minutes if not speaking English and using an interpreter), and will provide a discreet time
warning signal when one minute of presentation time remains. The team will be asked to
cease presenting when the time limit has been reached. At the conclusion of the teams’
presentation time, the Judges may choose to provide some feedback and / or ask any
clarifying questions they feel necessary.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 28 of 54 23 April 2025
C8.5 Verbal presentation judging provisions
STEM Racing™ will provide a dedicated private space, such as a small meeting room, where
each team will deliver their presentation to the Judges. This space will include a data projector
and screen, or LCD screen and multimedia sound system. These will be in fixed positions but
usually with sufficient cable length to allow teams some freedom for choosing where they wish
to locate their laptop. A single table will also be made available with its use and location in the
presentation space being optional.
C8.6 Verbal presentation video recordings
The Verbal Presentations of all teams will be used for the purpose of judging review and/or
may be used for post event publicity and promotional purposes by STEM Racing™ .

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 29 of 54 23 April 2025
ARTICLE C9 – RACING (250 points) UNDER REVIEW
C9.1 What races will be conducted?
The STEM Racing™ World Finals racing points will be awarded through the staging of two
types of race events:
• Reaction Racing – manual / driver launch mode, 8 races in total, each car will race in
each lane once over the 4 sessions.
• Knock-out Competition Races – manual / driver launch mode, one race in each lane
per round of competition (Qualification for the Knock-out, please see C9.7.1).
Reaction racing will be split over four sessions of two races. The average 'car race time' value
from all reaction races will determine the Fastest Car Award (refer C9.6). The knock-out
competition is the last of the scheduled races. Refer to ARTICLE C3.5 and further information
following for details on how points are calculated and awarded.
C9.2 Team preparation
C9.2.1 Teams should be familiar with the operation of the STEM Racing™ Race System.
There will normally be a section demonstration track within the venue where teams
can practice race starts during free time prior to their scheduled races.
C9.2.2 Manual / driver starts - One or more team members (driver/s) must be appointed for
launching of their team’s car using the manual launch method. Each lane of the track
has a dedicated starting area 1m x 1m which shall be clearly marked on the floor. The
driver must only make contact with the floor within this dedicated area and must not
touch or lean on the track.
C9.2.3 Finish line management - At least one member of the team must be appointed as
responsible for managing the finish line Car Deceleration System (refer C9.11), and
return of car along the track to the start.
C9.2.4 Start line car staging – Race Judges will be responsible for staging the car at the start
line. Team members are not permitted to adjust the car’s alignment themselves but
may request a single realignment by the judges. Under no circumstances may team
members interfere with the Power Unit Cartridge or the vertical alignment of the start
box. At the end of the staging process, all four wheels of the car must be in contact
with the track surface.
C9.2.5 Teams must ensure that both cars are race ready, a car service session will be
provided before the next race event (refer C10.2). If a teams’ car is damaged beyond
achievable repair then teams will forfeit any races that the car would have been used
for.
C9.3 Who needs to attend?
All team members must be present during their scheduled racing sessions.
C9.4 Reaction race procedure
Cars are launched in manual / driver reaction mode during four racing sessions, each
comprising of two races total per team, two (2) races in each lane. The TOTAL RACE TIME
displayed and the REACTION TIME displayed for each race is recorded. The reaction races
will be conducted as follows:
a) Teams race in order as shown in the competition programme. To begin racing, the
lowest team number will start in lane 1. All cars will be loaded onto the track, Car A
first then Car B.
b) One team member to track finish for deceleration system control.
c) Judge arms Start Box - SAFETY ON.
d) Race 1 (Car A) - Judge sets cars on track/tether line and inserts Power unit cartridge
– makes initial start box adjustments.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 30 of 54 23 April 2025
e) Please see C9.2.4 for more detail.
f) Driver and team stands trackside with corresponding lane start trigger.
g) Judge checks deceleration system is ready, all team members to stand in designated
safety zone as instructed by track judges, track is clear for racing, team information on
race system is correct, switches Start Box - SAFETY OFF.
h) Judge presses the start system reset button – cars are launched by driver pressing
start trigger.
i) Judge records TOTAL RACE TIME and REACTION TIME displayed on start gate.
j) Team member at finish moves car into storage zone at the end of the track.
k) Race 2 (Car B) conducted in same lane as above, driver can be inter-changed as
nominated.
l) Team member at finish control returns car and empty power unit cartridge along track
to the start with minimum handling.
m) Judges remove cars from tether line and change lanes, team information on race
system is correct.
n) Cars removed from track and returned to Parc Fermé.
C9.5 Reaction race scoring
All eight (8) ‘total race times’ recorded from the reaction races are considered. The fastest of
these eight (8) times is used in the following formulae to calculate the points awarded:
• Fastest ‘total race time’ = 105 pts
• 2
nd fastest ‘total race time’ = 100 pts
• 3
rd fastest ‘total race time’ = 95 pts
• Slowest ‘total race time’ = 5 pts
• Base Time = 120% of 3rd fastest ‘total race time’
• 4
th fastest and all other teams score points using the following formula:
• Team Points = 5 + (90 / (Base Time – fastest ‘total race time’)) x (Base Time – teams
fastest ‘total race time’)
• Any team with a best ‘total race time’ that is slower than the base time will score 5
points. To further discriminate between any teams scoring 5 points, a deduction of 1
point will be made for any did not finish (DNF) reaction race result.
C9.6 Time trial race scoring
The eight (8) ‘car race times’ recorded during racing will be considered. From these eight (8)
races, the team’s 2nd, 3rd, 4th and 5th best ‘car race times’ will be averaged. This average time
is used in the following formulae to calculate the points awarded:
• Fastest average (avg.) time = 105 pts
• Second fastest avg. time = 100 pts
• Third fastest avg. time = 95 pts.
• ‘Base Time’ = 115% of the third fastest avg. time of all teams avg. times.
• Fourth (4th) to slowest avg. time score points using the following formula:
Team Points = 20 + (75/(Base Time – 3
rd fastest avg.)) x (Base Time – teams avg.)
• Any team that has an average slower than the base time will score 20 points. To further
discriminate between these teams, a deduction will be made of 2.5 points for any did
not finish (DNF) time trial result.
• If after discarding a team’s fastest time there remains less than 4 times from races
finished, due to DNF’s, the slowest time recorded is again input to the average
equation until there are a total of four times to average.
C9.6.1 Fastest Car Race Time Bonus
A 10-point bonus will be awarded to the team with the single fastest ‘car race time’
value from all time-trial races.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 31 of 54 23 April 2025
C9.7 Knock-out Competition
Teams will take part in a knock-out (single elimination) competition. Teams will be issued the
knock-out competition seeding and competition bracket prior to the race event commencing.
The number of participating teams will be confirmed closer to the event.
C9.7.1 Seeding - The seeding order for the first knock-out round is determined through
seeding all teams using the average fastest ‘total race time’ they achieved from the
time trial racing event.
Cars judged to have performance regulation failures will have 0.5 seconds per
performance regulation failure per car added on to their fastest ‘total race time’ for
seeding purposes, see formula below:
𝑺𝒆𝒆𝒅𝒊𝒏𝒈 𝑻𝒊𝒎𝒆 =
(
𝑪𝒂𝒓 𝑨 𝒇𝒂𝒔𝒕𝒆𝒔𝒕 ‘𝒕𝒐𝒕𝒂𝒍 𝒓𝒂𝒄𝒆 𝒕𝒊𝒎𝒆’
+ (𝟎. 𝟓 × 𝑪𝒂𝒓 𝑨 𝑷𝒆𝒓𝒇𝒐𝒓𝒎𝒂𝒏𝒄𝒆 𝑹𝒆𝒈𝒖𝒍𝒂𝒕𝒊𝒐𝒏𝒔)
+ 𝑪𝒂𝒓 𝑩 𝒇𝒂𝒔𝒕𝒆𝒔𝒕 ‘𝒕𝒐𝒕𝒂𝒍 𝒓𝒂𝒄𝒆 𝒕𝒊𝒎𝒆’
+(𝟎. 𝟓 × 𝑪𝒂𝒓 𝑩 𝑷𝒆𝒓𝒇𝒐𝒓𝒎𝒂𝒏𝒄𝒆 𝑹𝒆𝒈𝒖𝒍𝒂𝒕𝒊𝒐𝒏𝒔)
)
𝟐
During knock-out racing teams will have 0.1 seconds per performance penalty per car
added to their pre-set reaction times.
C9.7.2 Knock-out competition procedure - During the knock-out competition BOTH race cars
will be used. Cars are launched in manual / driver reaction mode, with two (2) races
total, one (1) race in each lane, for each round of the knock-out. The team with the
fastest ‘total race time’, as displayed on the start gate, from the two races conducted,
is the winner of that knock-out round. In case of a tied result, a further ‘sudden death’
race will be conducted, this will be a repeat of race 2. The knock-out competition will
be conducted as follows:
a) Teams race in order of the competition draw. Top of draw in lane 1.
b) Prior to the cars being set on the track for each round, each team will be required to
nominate which car (A or B) they will use for their first race. Each teams’ other car will
be used for the second race.
c) One team member to track finish for deceleration system control.
d) Judge arms start box - SAFETY ON – makes initial start box adjustments.
e) Race 1 - Judge sets all cars on track / tether line and inserts power unit cartridge
f) A team member is then allowed 30 seconds to ‘fine tune’ the alignment of their car,
please see C9.2.4 for more detail. The deceleration system must also be set during
this time.
g) Driver stands trackside with corresponding lane start trigger.
h) Judge checks deceleration system is ready, all team members to stand in designated
safety zone as instructed by track judges, team information on race system is correct,
track is clear for racing, switches start box - SAFETY OFF
i) Judge presses the start system reset button – cars are launched by driver pressing
start trigger.
j) Judge records TOTAL RACE TIME displayed on start gate.
k) Team member at finish moves car into storage zone at the end of the track Judges set
cars for Race 2.
l) Check team information on race system is correct
m) Race 2, driver can be inter-changed.
n) Cars removed from track and returned to Parc Fermé.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 32 of 54 23 April 2025
C9.7.2 Knock-out competition scoring example. This will depend on the number of competing
teams.
Points are awarded based on the round of competition a team is eliminated as follows:
• Seeded outside top 32 = 2 pts
• Eliminated in Round 1 (Round of 32) = 6 pts
• Eliminated in Round 2 (Round of 16) = 8 pts
• Eliminated in Quarter Final = 15 pts
• Eliminated in Semi Final = 22 pts
• Eliminated in Final = 26 pts
• Knock-out Winner = 30 pts
C9.8 DNF (Did not Finish) race results
Damage or part separation occurring during a race, before the car crosses the finish line, (e.g.
wheel or any other part of the car separating), or a car not crossing the finish line at all, effects
in a DNF race result. The Judges may refer to video evidence to verify a DNF result.
C9.9 False Starts
C9.9.1 A false start (jump start) occurs when the driver depresses the trigger button before
the 5 start gate lights have extinguished. The screen will display a false start
message.
C9.9.2 All reaction false starts will incur a 2.5 point penalty and by default forfeit that race.
This penalty does not apply to knock-out racing.
C9.9.3 During knock-out racing – If one team false starts (jump starts), the other team should
continue to race as normal. The team who false started forfeits that race, scoring a
DNF, and the other team’s time is recorded. If both teams false start, the race counts
as one of the two (2) runs.
C9.9.4 During any manual / driver starts, if a driver false starts and distracts the other driver
the race will be re-run and the driver who caused the distraction will forfeit their race.
C9.9.5 Distractions outside of the race start area will be assessed by the lead track judge
and track officials to determine if the race should be re-run. All competitors must, and
other spectators will be instructed to, keep noise down to a minimum and to not use
flash photography.
C9.10 Track, tether line and timing system information
C9.10.1 The STEM Racing™ Elevated Race Track, supplied by Denford Ltd will be used.
The official length of the track, from start line to finish is 20 metres. A monofilament
tether line of diameter 0.6mm, fixed at the finish end, passes down the centre of
each lane. At the start end the line passes through 90 degrees over a single pulley
then attached to a 1.0kg mass suspended above the floor.
IMPORTANT: Teams are not permitted to add anything to the race track or
race system. This includes the car staging area.
C9.10.2 Launch/Timing - The STEM Racing™ Launch/Timing System will be used for
launching cars and timing races and driver reaction times to 1/1000th of a second.
C9.11 Car Deceleration Systems
C9.11.1 Teams must use the Halo deceleration system. The Halo Deceleration System acts
to bring cars to rest once crossing the finish line. STEM Racing™ will provide a Halo
Deceleration System which is integrated into the final track section after the finish line. This
consists of an arresting cable which is aligned with the circular notch of the Halo. If a team
fails T4.4.4 Halo notch height they will be required to use the Brushes Car Deceleration
System.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 33 of 54 23 April 2025
C9.11.2 The final 350mm of the track after deceleration systems is reserved for a storage
zone to store raced cars before they are returned to the track start.
C9.12 Race Power Packs
Compressed gas cartridges to be used for all World Finals competition races will be supplied
by STEM Racing™. Each race cartridge will be separately weighed before competition to
ensure that all race cartridges used for races are within a weight range of 0.5 grams. All race
cartridges will be kept in a temperature-controlled environment of 21 degrees Celsius.
C9.13 Car weight checks
Cars will have their weight checked at the race track prior to commencing a race event. This
is done to ensure each car remains at a legal weight during all races. If a car is judged to have
gone under weight whilst stored in parc fermé, the Judges will add ballast to return the car
weight to what it was when first submitted to parc fermé, without penalty.
C9.14 Judges handling cars
The race Judges will not be required to comply with any special car handling requests made
of them by teams. This includes use of any special gloves or tools.

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 34 of 54 23 April 2025
ARTICLE C10 – CAR REPAIRS AND CAR SERVICING
C10.1 Car repairs
C10.1.1 All damage issues and related repair work during racing is at the Judge’s discretion
and may be referred to the scrutineering Judges and/or Chair of Judges for a final
decision.
C10.1.2 No items can be removed or added to a car during racing, other than Power unit
cartridges, except in the case of a repair.
C10.1.3 No penalty is applied for damage incurred during knock-out racing or a car’s final race
of any race event.
C10.2 Car servicing
C10.2.1 Teams will be scheduled time to carry out penalty-free maintenance and repairs on
their race cars in the designated car service area. There will be a car service session
after each race session. The duration of each car service session will be confirmed
closer to the event.
C10.2.2 A shorter car service session will be allowed between further rounds of the knockout
competition.
C10.2.3 Only team members and Judges are allowed to enter the car service area.
C10.2.4 Tool kits are allowed to be taken into car service. Teams must supply all of their own
tools and other necessary resources. Judges will not be able to assist teams with any
additional resource requirements.
C10.2.5 Maintenance and alterations can only be made to the front and rear wings, nose cone,
tether line guides, wheels and wheel support systems. The car body MUST NOT be
modified or substituted.
C10.2.6 Each team will be required to complete a car service log form, declaring any
maintenance or repair work completed. This will be validated by the Judges.
C10.2.7 Teams must hand their race cars and completed car service log to the service area
Judges BEFORE the conclusion of their scheduled service interval. A penalty will
apply for exceeding the scheduled service time limit of 5 points for every minute late.
Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 35 of 54 23 April 2025
ARTICLE C11 – PROTESTS
C11.1 Scrutineering decision appeals
These must be submitted within two hours of the team completing their specification review
judging. Other rules for submitting these will be the same as for protests.
C11.2 Submitting a protest
Any protest issues must only be submitted by the team manager by email (globaladmin@stemrcaing.com) to an Event Director, who will register this and immediately submit
it to the Chair of Judges. This must occur no later than 21:00 (local time) on racing day 2. Any
protest or appeals submitted after this time may be disregarded. The Chair of Judges decision
related to any protest is final.
C11.3 Unsuccessful protests
Teams should carefully consider their grounds for submitting a protest or appeal.
Any protest or appeal that is unsuccessful, with the Judges initial decision remaining
unchanged, will result in the team having a 15-point penalty applied against their total score.
THE CHAIR OF JUDGE’S DECISION IS FINAL

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 36 of 54 23 April 2025
ARTICLE C12 – JUDGES
C12.1 Overview
There will be six (6) teams of Judges plus officials that form the entire judging panel. Each
judging team will have one Judge appointed as the Lead Judge. Judges are nominees from
ICC’s and other education and industry experts invited by STEM Racing™. All Judges sign a
‘declaration’ and code of conduct to ensure there are no conflicts of interest with respect to
Judges and the teams they are judging.
C12.2 Chair of Judges
An independent authority appointed by STEM Racing™ to oversee all judging procedures.
The Chair of Judges will determine the final judging decision where a protest has been
submitted or other judging issue needs resolution. The Chair of Judges will also preside over
a meeting of all Lead Judges to ratify the final results along with nominations and winners for
relevant awards.
C12.3 The Judging teams
C12.3.1 Specification & Scrutineering Judges - will assess both race cars plus the rendered
images and engineering drawings as per the Specification & Scrutineering
scorecards.
C12.3.2 Design & Engineering Judges - will assess each team as per the Design &
Engineering scorecard.
C12.3.3 Verbal Presentation Judges – will assess each team as per the Verbal Presentation
scorecard.
C12.3.4 Project Management– will assess each team as per the Project Management
scorecard.
C12.3.5 Enterprise Judges – will assess each team as per the Enterprise and Pit Display
and Team identity scorecards.
C12.3.6 Race officials – will oversee and rule on all race events and any incidents.
C12.3.7 Car servicing officials – will oversee all car service activities and rule on any
infringements that may occur.
C12.4 Judging Decisions
THE DECISION OF THE JUDGES AND OFFICIALS IS FINAL.

Aramco STEM Racing World Finals 2025 - Competition Regulations
©2025 – STEM Racing™ Ltd. Page 37 of 54 23 April 2025
ARTICLE C13 - AWARDS
C13.1 Awards Celebration
The World Finals awards will be presented at the Awards Celebration Gala Dinner. Details of
this event will be released closer to the event.
C13.2 Participation Recognition
All students will receive an official participation certificate.
C13.3 Prizes and Trophies
C13.3.1 Formula 1® Team Trophies – In past years STEM Racing™ has been extremely
fortunate to have all Formula 1® teams generously supply purpose built ‘ONE OFF’
trophies for various awards. These trophies are unique and some are constructed
from Formula 1® car components.
C13.3.2 Awards – Teams that win an award will be presented with a SINGLE main trophy
or similar memento and the team members and / or supervising teacher will need to
decide how this memento is to be shared and displayed amongst the team
stakeholders.
C13.3.3 Student mementos – students winning an award may be presented with their own
individual medallion or certificate.
C13.3.4 STEM Racing™ World Champions Trophy – This is a perpetual trophy presented to
the World Champions, and as such, must be returned to STEM Racing™ before the
following years World Finals event. Our Title partner, Aramco will also be providing
a World Champions trophy for the winner to keep forever.
C13.4 List of awards to be presented
All awards below will be presented to the team that achieves the highest score in each
category taken from the scorecards unless otherwise indicated (*) below. (this list may be
amended at the discretion of STEM Racing™).
1. World Champions – STEM Racing™ World Champions
Trophy
2. 2
nd Place
3. 3
rd Place
4. Best International Collaboration Team Award
5. Best Newcomer Award
6. Best Engineered Car Award
7. FIA Scrutineering Award
8. Sponsorship & Marketing Award*
9. Innovative Thinking Award*
10. Chair of Judges Recognition of Achievement Award*
11. Research and Development Award*
12. Fastest Car Award
13. Team Identity Award*
14. Pit Display Award*
15. Verbal Presentation Award*
16. Project Management Award*
17. Digital Media Award*
18. Knockout Competition Winners
19. FIA Women in Motorsport Award*
20. Sustainability Award*
21. Fastest Nose Change Award
22. Autodesk AI (Generative design)
Award
STEM Racing - 2025 World Finals Competition Regulations
©2025 – STEM Racing™ Ltd. Page 38 of 54 23 April 2025
APPENDIX…
1. Awards Matrix
2. 2025 World Finals Scorecards
3. Race Procedure & Troubleshooting Flowchart
4. Pit Display Reference Dimensions
5. Project Submission Checklist
6. Table of contents for engineering drawings
STEM Racing - 2025 World Finals Competition Regulations
©2025 – STEM Racing™ Ltd. Page 39 of 54 23 April 2025
Awards Matrix
Please find below a matrix that shows which judging categories contribute towards each award:
Judges Heading Sub Heading
World Champions
2nd Place
3rd Place
Best International Collaboration
Best Newcomer
Best Engineered Car
FIA Scrutineering Award
Sponsorship & Marketing Award
Innovative Thinking Award
Team Identity Award
Pit Display Award
Verbal Presentation Award
Sustainability Award
Research & Development Award
Digital Media Award
Project Management Award
Fastest Car Award
Scrutineering Scrutineering
Specifications ● ● ● ● ● ● ●
Engineering Drawings ● ● ● ● ● ●
Rendering ● ● ● ● ● ●
Quality of Finish and Assembly ● ● ● ● ● ●
Design & Engineering
Design &
Engineering
Portfolio
Design Concepts ● ● ● ● ● ●
3D Modelling ● ● ● ● ● ●
Application of CAA ● ● ● ● ● ● ●
Use of CAM/CNC ● ● ● ● ● ●
Other Manufacturing & Assembly ● ● ● ● ● ●
Research & Development ● ● ● ● ● ● ●
Testing ● ● ● ● ● ● ●
Design Process Evaluation ● ● ● ● ● ●
Document Presentation ● ● ● ● ●
Project Management
Initiating
Initiation Process ● ● ● ● ● ●
Project Schedule ● ● ● ● ● ●
Planning
Budget and Resource Management ● ● ● ● ● ●
Roles and Responsibilities ● ● ● ● ● ●
Executing
Team & Stakeholder Comm. ● ● ● ● ● ●
Risk Management ● ● ● ● ● ●
Mon. and Cont. Monitoring & Controlling ● ● ● ● ● ●
Enterprise
Enterprise
Marketing Strategy & Materials ● ● ● ● ● ● ●
Sponsorship & return in Investment ● ● ● ● ● ● ●
Digital Media Proficiency ● ● ● ● ● ● ●
Sustainability ● ● ● ● ● ●
Document Presentation ● ● ● ● ●
Team Identity Overall Team Identity ● ● ● ● ● ● ●
Pit Display
Pit Display Design Process ● ● ● ● ● ●
Pit Display Content Clarity and Impact ● ● ● ● ● ●
Functionality & User Experience ● ● ● ● ● ●
Verbal Presentation
Technique
Engagement & Presentation ● ● ● ● ● ●
Team Contribution ● ● ● ● ● ●
Composition
Content Quality, Relevance & Subject ● ● ● ● ● ●
Time, Clarity and Structure of Content ● ● ● ● ● ●
Subject
Innovation ● ● ● ● ● ● ●
Collaboration ● ● ● ● ● ●
STEM Racing™ Learning Experiences ● ● ● ● ● ●
Racing Racing
Time Trials ● ● ● ● ● ●
Reaction ● ● ● ● ● ●
Damage During Racing ● ● ● ● ● ●
©2025 – STEM Racing™ Ltd. Page 40 of 54 23 April 2025
Scrutineering Judging Scorecard
Team Number:
Team Name:
Country:
Scrutineering
Engineering
Drawings
Little or no detail,
Little or no
annotation.
No table of
contents.
No regulation
compliance was
shown.
Basic views included.
Some dimensions are
included but not sufficient
annotations.
Insufficient regulation
compliance was shown.
A basic table of contents.
Multiple views including
First or Third-angle
orthographic projection
matching the final car.
Some parts or materials are
represented.
Some Regulation
compliance shown (eg T.
4.2 Virtual Cargo
identification.)
Good table of contents.
First or Third-angle orthographic
projection matching the final car and
unrendered isometric view or
similar. Additional views to show
sufficient detail.
Parts list/bill of materials.
Excellent regulation compliance
shown (eg T.4.2 Virtual Cargo
identification.)
Complete and ordered table of
contents.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Rendering
Poor quality
renders.
Insufficient views.
Multiple views.
Some inconsistencies
matching the final car.
Multiple views.
Good match to the final car
Good render technique.
Multiple views. Perfect match to the
final car including branding.
Realistic environment and lighting
High-end render technique.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Quality of Finish
and Assembly
Poor finish and
assembly.
No justification for
intended quality
and finish
documented in the
final page of the
engineering
drawings
document.
Reasonable finish with some
inconsistencies.
Reasonable assembly.
Some justification for
intended quality and finish is
documented in the final page
of the engineering drawings
document.
Good overall intended
finish. Intended quality and
assembly with attention to
detail.
Justification for intended
quality and finish is well
documented in the final
page of the engineering
drawings document.
Intended quality, assembly and
finish on all components is
exceptional. The two cars are
identical.
Justification for intended quality and
finish is comprehensively
documented in the final page of the
engineering drawings document.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Scrutineering Total = /60
Notes:
©2025 – STEM Racing™ Ltd. Page 41 of 54 23 April 2025
Design & Engineering Scorecard
Team Number:
Team Name:
Country:
Design & Engineering Portfolio Only Assessment
Design Concepts
Single or minimal concepts
for car components with no
links to research. No
relevance to final car.
Basic concepts of car
components with limited links to
research. Limited relevance to
final car.
Good technically inspired ideas
that are relavent for different car
components linked to research.
Excellent technically inspired
ideas for multiple car components
with research-detailed. Relevance
of the concept strongly justified.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
3D Modelling
Minimal application of 3D
modelling techniques. Only
final design 3D modelled.
Basic use of 3D modelling tools
and techniques.
More than 1 design included
with different iterations.
Good use of advanced 3D
modelling tools, showcasing
skill and technique. Dimensional
constraints of the STEM
RACING model block
considered. Design approach
explained.
Design for manufacture
considerations noted. (ie fillets,
tolerance of machining).
Expert use of a wide range of
complex 3D modelling techniques,
demonstrating exceptional skill
and innovation.
Design for manufacture directs
process. (ie machining tool
availability, fit clearances).
Quality of CAD surfaces analysed.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Application of
Computer Aided
Analysis
Poor choice and no
justification of simulation
parameters.
Weak analysis with poorly
presented/no results.
No design choices made
based on FEA/CFD study.
Limited choice and justification
of simulation parameters.
Limited analysis and results.
Little to no design choices made
based on FEA/CFD study.
Well-justified choice and
understanding of simulation
Good analysis with clear, wellpresented results.
Some design choices made
based on FEA/CFD study.
Excellent choice & understanding
of simulation parameters.
Detailed analysis with clear, wellpresented results.
Proven design improvements
made based on FEA/CFD study.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Use of CAM/CNC
No or minimal evidence of
CAM/CNC understanding or
manufacturing.
Basic evidence of CAM/CNC
processes and manufacturing.
Good use and understanding of
CAM/CNC processes to achieve
manufacturing goals.
Manufacturing issues noted with
limited problem solving.
Evidence of excellent
understanding of CAM/CNC
technologies. Appropriate
techniques and processes used to
achieve manufacturing goals.
Manufacturing issues discussed
with innovative problem-solving
solutions.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Other
Manufacturing &
Assembly
No or minimal manufacturing
presented.
No or minimal consideration
of quality assurance and
workplace safety
documented.
No or minimal justification of
outsourcing.
The manufacturing process is
mentioned without detail.
Basic consideration of quality
assurance and workplace safety
documented.
Basic justification of
outsourcing.
Good manufacturing process
and stages described.
Good consideration of quality
assurance and workplace safety
documented.
Appropriate use of
manufacturing resources
documented (i.e. tools, finishes,
jigs, fixtures).
Outsourcing clearly explained
and justified.
Details all manufacturing stages
and processes.
Quality assurance and workplace
safety considerations evident.
Appropriate outsourcing justified
with make vs buy analysis.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Research &
Development
No or limited evidence of
R&D.
Basic evidence of R&D with
some principles considered.
Some scientific & mathematical
theories and principles
considered. Logical research
based design developments
explained and justified.
Relevant R&D throughout the
entire product design &
development cycle. Design
concept developments refined and
justified from research & test
findings.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Testing
No or little evidence of testing
on the fully assembled car
and individual components.
Limited testing.
Some evidence of method and
outcomes on the fully
assembled car and individual
components.
Good testing. Different evidence
of method and outcomes.
Some evidence of virtual and
physical testing on the fully
assembled car and individual
components.
Appropriate testing with excellent
methods and outcomes
documented.
Comprehensive evidence of virtual
and physical testing on the fully
assembled car and individual
components.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Design Process
Evaluation
No or limited Ideas or process
evaluations at different
stages.
No or limited documentation
of evaluation-linked
improvement actions.
Basic Ideas or process
evaluations at different stages.
Basic documentation of
evaluation-linked improvement
actions.
Multiple Ideas or process
evaluations at different stages.
Good documentation of
evaluation-linked improvement
actions.
Excellent ongoing idea evaluations
linked to improvement actions.
Comprehensive documentation of
evaluation-linked improvement
actions.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Document
Presentation
Difficult to follow with basic
presentation standard.
Basic organisation. Good and clear structure, well
organised.
High impact and professional
throughout.
Consistent and clear organisation.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Design & Engineering Portfolio Only Assessment Total = /180
Notes:
©2025 – STEM Racing™ Ltd. Page 42 of 54 23 April 2025
Project Management Scorecard
Team Number:
Team Name:
Country:
Project Management Assessment
Initiating
Initiation
Process
No or limited
evidence of an
Initiation process.
Evidence of an Initiation
process with goals and
deliverables identified,
leading to a basic scope
statement.
Evidence of an Initiation process
including Kick-off meeting. Project
charter created with goals and
deliverables identified. Good
scope statement developed,
identifying acceptance criteria for
each deliverable.
Kick-off meeting evidenced. Detailed Project
Charter created, clearly defining all deliverables.
Comprehensive scope statement developed,
identifying acceptance criteria for each deliverable.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Project
Schedule
No or limited
evidence of tasks to
be completed.
Evidence of a project
schedule, showing a
breakdown of time
required to complete
essential tasks.
Clear evidence of a project
schedule and Work Breakdown
Structure. Detailed Gantt chart
created to identify all tasks,
dependencies, and time
estimations. Resource allocation
is included for major project
phases.
Comprehensive project schedule with detailed
Work Breakdown Structure and Gantt chart. All
tasks, dependencies, and time estimations are
clearly identified. Key dependencies are identified,
and critical path analysis is included.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
Initiating Total /35
Planning
Budget and
Resource
Management
No or limited
evidence of
strategies to
manage budget
and/or resources.
Some evidence of
resources required and
how they are to be
acquired and managed.
Some evidence of
budgeting.
Clear evidence of budgeting and
use of basic accounting methods
to track expenditure. Identification
of where, when, and how
resources are to be acquired and
used. Initial cost estimates for
major project components.
Comprehensive budgeting with detailed cost
breakdown and methods for tracking expenditure.
Thorough resource management plan, including
procurement strategies, resource allocation, and
utilization forecasts. Cost-benefit analysis for key
project decisions.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
Roles and
Responsibilities
No or limited
evidence of clear
roles and
responsibilities
within team.
Team roles and
responsibilities identified,
with some evidence of
task and/or activity
breakdown.
Team members identified and a
structured team created with
defined job functions and
appropriate responsibilities.
Evidence of a basic Responsibility
Assignment ('RACI') Matrix.
Highly structured team with clearly defined job
functions, skill requirements, and detailed
responsibilities. Comprehensive RACI Matrix
covering all project activities. Evidence of a team
development plan and strategies for managing
team dynamics.
0 1 2 3 4 5 6 7 8 9 10
Planning Total /25
Executing
Team &
Stakeholder
Communications
No or limited
evidence of
engagement
between team
members and
stakeholders.
Evidence of a
communication plan and
engagements between
team members and with
stakeholders.
Clear communication plan
implemented between team
members and stakeholders. Key
stakeholders registered and
reported to regularly. Multiple
communication tools used
effectively.
Comprehensive communication strategy with
tailored approaches for different stakeholder
groups. Regular, documented communication with
all stakeholders using diverse, appropriate
channels. Evidence of feedback loops and
continuous improvement in communication
processes. Stakeholder engagement matrix
utilized to manage relationships.
0 1 2 3 4 5 6 7 8 9 10
Risk
Management
No or limited
evidence of risk
identification and
management.
Evidence of risk
identification and
response management
plans in place.
Clear evidence identifying all
relevant risks, area(s) of impact
and response planning.
Assessment of impact on
resources, timing, scope and
quality.
Comprehensive risk management strategy
including detailed risk register, risk analysis, and
prioritization. Proactive risk strategies implemented
with contingency plans. Regular risk reviews and
updates throughout the project lifecycle. Evidence
of opportunity management alongside risk
management.
0 1 2 3 4 5 6 7 8 9 10
Executing Total /20
Monitoring and Controlling
Monitoring &
Controlling
No or limited or
isolated project
evaluation.
Ongoing evaluation of
most areas. Documented
evidence of problems
identified and suggested
solutions.
Regular 'Status Reports',
documenting tasks signed off and
highlighting areas of concern.
Scope creep identified with a clear
action plan for tasks that overrun.
Key performance indicators (KPIs)
tracked and reported.
Regular and detailed project tracking processes
consistently applied. Comprehensive 'Status
Reports' include: Analysis of work completed
versus resources used, Comparison of planned
versus actual progress, Predictions of future
project performance, Clear procedures for
managing project changes, with all modifications
documented.
0 1 2 3 4 5 6 7 8 9 10
Monitoring and Controlling Total /10
Initiating + Planning + Executing + Monitoring and Controlling = Project Management Total = /90
Notes:
©2025 – STEM Racing™ Ltd. Page 43 of 54 23 April 2025
Enterprise Scorecard
Team Number:
Team Name:
Country:
Enterprise Portfolio Only Assessment
Marketing
Strategy &
Materials
Lack of coherent
marketing strategy,
poorly developed
marketing materials,
and minimal content
relevance.
Partially coherent marketing
strategy, average quality
marketing materials, needs
enhancement in content
relevance.
Good marketing strategy,
reasonably developed
marketing materials, and
satisfactory content
relevance.
Well-defined marketing
strategy, high-quality
marketing materials, and
highly relevant content.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Sponsorship &
Return on
Investment (ROI)
No or incomplete
Sponsor/partner
hierarchy.
Limited understanding
of sponsorship.
No evidence of ROI.
Basic Sponsor/partner hierarchy
and benefits included.
Partial understanding of
sponsorship.
Some evidence of return of
investment (ROI) to relevant
sponsors.
A range of sponsor/partner
hierarchy and benefits
identified. Good
understanding of
sponsorship, reasonable
investment, and satisfactory
ROI to relevant sponsors.
Sponsor/partner hierarchy and
benefits detailed and justified.
Range of relevant
sponsors/partners showing
mutually beneficial
relationships.
Creative activities linked to
return of investment (ROI).
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Digital Media
Proficiency
Limited understanding
and utilization of digital
media platforms.
Minimal engagement
with audience, and
ineffective content
creation.
Partial understanding and use of
digital media platforms.
Some evidence of strategy
documented.
Audience engagement needs
improving.
Good understanding and
utilization of digital media
platforms. Good execution
in line with documented
strategy. Reasonable
engagement, and content
creation.
Strong understanding and
effective utilization of digital
media platforms in line with
documented plans.
High audience engagement,
and impressive content
creation.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Sustainability
No or limited
understanding and
implementation of
sustainable practices.
No or minimal
awareness of
environmental impact.
Partial understanding and
inconsistent implementation of
sustainable practices.
Needs improvement in awareness
of environmental impact.
Some evidence of
implementation.
Good understanding and
moderate implementation of
sustainable practices.
Some awareness of
environmental impact.
Implementation documented
considering different factors
such as economic,
environmental, and social.
Strong understanding and
effective implementation of
sustainable practices.
High awareness of
environmental impact and
active involvement in
sustainability initiatives
considering economic,
environmental, and social
factors.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Document
Presentation
Poor formatting, lack of
structure.
Minimal visual appeal in
the document.
Average formatting with some
structure.
Needs improvement in the
document visual appeal.
Good formatting, structured
document.
Satisfactory document
visual appeal.
Good organisation.
Excellent formatting, wellstructured document, and
highly appealing visually.
High impact and professional
throughout.
Consistent and clear
organisation.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Enterprise Portfolio Only Assessment Total /100
Notes:
©2025 – STEM Racing™ Ltd. Page 44 of 54 23 April 2025
Pit Display & Team Identity Scorecard
Team Number:
Team Name:
Country:
Pit Display Assessment
Pit Display
Design Process
(Documented in
Enterprise
portfolio)
Limited planning and
execution, lack of
innovation, and minimal
attention to detail in the
design process.
Some planning and execution.
Insufficient innovation.
Needs improvement in attention to
design details.
Some ideas development
documented.
Different ideas & justification
of design.
Good evidence of
development considering
factors including team
identity, budget,
sustainability and time
constraints with
consideration to functionality
and user experience.
A range of ideas, clearly
justified, creative final design.
Comprehensive evidence of
development considering
factors including team identity,
budget, sustainability and time
constraints with consideration
to functionality and user
experience.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Pit Display
Content Clarity
and Impact
Repetition of Portfolio
contents.
Disorganised layout.
Little or no evidence of
marketing materials.
Minimal information
about the team's work.
Partially informative content.
The pit display is not enhanced by
Multimedia or Marketing materials.
The Pit display needs more clarity
detailing the team's work.
Good organisation and
impact.
Multimedia is used to
enhance the display, with
some marketing material on
display.
Clear and effective
presentation and messaging
about the team’s work.
Clean, well-organised with
high impact. Highly
professional with attention to
detail.
Excellent integration of
technology, multimedia and
marketing materials.
Comprehensive information
about the team's work.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Functionality &
User Experience
execution
Non-functional or poorly
functional design,
inconvenient user
experience.
Lacks impact, and
minimal overall visitor
impression.
Basic functionality, average user
experience, needs improvement in
functionality and overall visitor
impression.
Good functionality, and
satisfactory user
experience.
Innovative Pit display and
positive visitor impression.
Excellent functionality,
seamless user experience,
and impressive innovation
across the Pit Display.
A very positive impression on
visitors.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Pit Display Total = /60
Team Identity
Overall Team
Identity
Inconsistent, limited or
obscure identity through
project elements.
Weak team cohesion,
lack of shared identity.
Partial team cohesion, and
inconsistent shared identity
through project elements.
Good team identity is
consistent through various
project components e.g. car
matches team uniform.
Excellent and highly effective
team identity. Team ‘brand’
consistently applied through
all project elements.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Team Identity Total /20
Pit Display Total + Team Identity Total = /80
Notes:
©2025 – STEM Racing™ Ltd. Page 45 of 54 23 April 2025
Verbal Presentation Scorecard
Team Number:
Team Name:
Country:
Technique
Engagement &
Presentation
Dynamics
Monotonous
presentation, lack of
visual aids, and minimal
interaction with audience.
Poor delivery technique.
Limited team dynamics,
some visual aids.
Limited delivery technique
and interaction with the
audience.
Good team dynamics,
effective visual aids,
Good delivery and
interaction with the
audience.
Excellent engagement,
captivating and highly
interactive delivery, and
strong audience
connection.
Exceptional team
dynamics, and impactful
visual aids.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Team Contribution
Single team member
taking the lead in
presentation.
Minimal team
participation during the
presentation.
Good contributions from
most team members.
Excellent teamwork with all
members participating
effectively.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Technique Total /40
Composition
Content Quality,
Relevance & Subject
Understanding
Irrelevant or outdated
content, lack of depth,
and poor relevance.
Unclear explanations.
Partially relevant content,
some depth, needs
improvement in quality and
explanations.
Relevant content, good
depth, and reasonably highquality information. Clear
explanations.
Highly relevant content,
profound depth, and
exceptional quality
information with articulate
explanations.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Time, Clarity and
structure of content
Severe time
management issues, with
significant rushing or
excessive time taken.
Less than 8 minutes or
more than 12 minutes.
Incoherent structure,
unclear message, and
disorganised content.
Time management issues
are evident, with noticeable
rushing or excessive time
taken.
Less than 9 minutes or more
than 11 minutes.
Partially clear structure,
some coherence, needs
better content organisation.
Good flow and time
management of each topic
with minimal rushing or
excessive time taken.
Clear structure, coherent
flow, and organised content.
Excellent time
management and balance
of each topic without
exceeding the time limit.
Excellent structure, crystalclear message (concept),
and highly organized
content.
Excellent attention to
detail.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Composition Total /40
Subject
Innovation
Little project innovation
presented with no
justifications.
Average project innovations
are described but with no
justification.
Good project innovations
are described and justified
and connected to
competition elements.
Excellent innovations
related to competition
elements, or other aspects
with high positive project
impact.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Collaboration
None or Little
collaboration with
industry or higher
education mentioned.
Some collaboration with
industry or higher education
is mentioned.
Good description of
collaboration with industry
and higher education.
Excellent justification of
collaborations with industry
and higher education.
Links to learning and
project outcomes.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
STEM Racing™
learning journey
No or limited real
reflections discussed.
Basic explanation of some
learning outcomes for some
team members.
Good explanation of some
learning outcomes for all
team members.
A range of personal, lifelong learning and career
skills acquired and
identified as project
outcomes for all team
members.
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
Subject Total /60
Technique Total + Composition Total + Subject Total = Verbal Presentation Total = /140
Notes:
©2025 – STEM Racing™ Ltd. Page 46 of 54 23 April 2025
Specifications Scorecard
For clarification on individual regulations, refer to the World Finals Technical Regulations.
Please enter ✓ for a pass and F for a fail
(8g Pack) – measured with full 8g race power pack cartridges
Team Number:
Team Name:
Country:
Initial Scrutineering Amendments
Reg Regulation Overview Min/Max
Quick Guide
Penalty
per Car
Car
A
Car
B
CoJ
CS
Car
A
Car
B
CoJ
CS Remarks
ARTICLE T3 – FULLY ASSEMBLED CAR
T3.1.1 Designed and engineered using CAD / CAM -5
T3.1.2 Body manufactured using CNC only Check unfinished body -5
T3.1.3 F1 in Schools holographic sticker Must be supplied -5
T3.1.4 Race cars identical geometry Visual check -5
T3.2.1 Safe Construction – Specification judging Check T3.2.1 -10
T3.3 Defined features Check T1.1 -20
T3.4 Total width Min: 65 Max: 85 -5 mm mm
T3.5 Total height (8g Pack) Max: 65 -5 mm mm
T3.6 Total weight Min: 48.0g -10 g g
T3.7 Track clearance (8g Pack) Min: 1.5 -10
T3.8 Status during racing Nothing removed -5
T3.9
Replacement Components Identical to fitted
Nose Cone & Front Wing Assembly Max: 2 -5
Rear Wing Assembly Max: 2 -5
Front Wheels Max: 4 -5
Front Wheel Support Structure Max: 2 -5
Rear Wheels Max: 4 -5
Rear Wheel Support Structure Max: 2 -5
Page 1 Notes:
©2025 – STEM Racing™ Ltd. Page 47 of 54 23 April 2025
Specifications Scorecard
For clarification on individual regulations, refer to the World Finals Technical Regulations.
Please enter ✓ for a pass and F for a fail
(8g Pack) – measured with full 8g race power pack cartridges
Team Number:
Team Name:
Country:
Initial Scrutineering Amendments
Reg Regulation Overview Min/Max
Quick Guide
Penalty
per Car
Car
A
Car
B
CoJ
CS
Car
A
Car
B
CoJ
CS Remarks
ARTICLE T4 – BODY
T4.1 Body construction F1 Model Block only -20
T4.2 Virtual cargo – See T4.2 for dims Between axles -25
T4.3 Virtual cargo identification Check Eng. drawing -5
T4.4.1 Halo Halo exists -10
T4.4.2 Halo visibility front and side views Side & front view -10
T4.4.3 Halo visibility Refer to Article T1.21 -10
T4.4.4 Halo circular notch height 34.0 (±1.0) -5 mm mm
T4.4.5 Halo safety test 1kg test, safe to race -5
T4.5 Helmet Included -5
T4.6 F1 in Schools logo decal location Between Front & Rear
wheels 100% Visible -5
T4.7 Team Number Min: 8.0 -2
T4.8 Decal Thickness Max: 0.5 -5
ARTICLE T5 – RACE POWER PACK CARTRIDGE CHAMBER
T5.1 Diameter Min: 18 Max: 18.5 -5
T5.2 Distance from track surface (8g Pack) Min: 30 Max: 40 -5
T5.3 Depth Min: 45 Max: 58 -5
T5.4 Max angle of chamber (8g Pack) Min: -3° Max: 3° -5
T5.5 Chamber safety zone (8g Pack) Min: 3 -10
T5.6 Power unit cartridge visibility (8g Pack)
Min: 5mm
top view -10
ARTICLE T6 – TETHER LINE GUIDES
T6.1 Location 10mm in front / front axle
10mm behind / rear axle -10
T6.2 Internal diameter Min: 3.5 Max: 6 -5
T6.3 Tether line guide safety 200g test, safe to race -10
Page 2 Notes:
©2025 – STEM Racing™ Ltd. Page 48 of 54 23 April 2025
Specifications Scorecard
For clarification on individual regulations, refer to the World Finals Technical Regulations.
Please enter ✓ for a pass and F for a fail
(8g Pack) – measured with full 8g race power pack cartridges
Team Number:
Team Name:
Country:
Initial Scrutineering Amendments
Reg Regulation Overview Min/Max
Quick Guide
Penalty
per Car
Car
A
Car
B
CoJ
CS
Car
A
Car
B
CoJ
CS Remarks
ARTICLE T7 – WHEELS AND WHEEL SUPPORT STRUCTURES
T7.1 Number and location 4, 2 x 2 -25
T7.2.1 Distance between opposing wheels – Front Front Min: 38 -2.5
T7.2.2 Distance between opposing wheels – Rear Rear Min: 30 -2.5
T7.3 Wheelbase Min: 120 Max: 140 -5
T7.4 Track contact width
Front Min: 13
Rear Min: 17
exc. chamfer/fillet
-2.5
per
wheel
FL: mm FL: mm
FR: FR:
RL: mm RL: mm
RR: RR:
T7.5 Diameter Min: 28
Max: 32
-2.5
per
wheel
FL: mm FL: mm
FR: FR:
RL: mm RL: mm
RR: RR:
T7.6 Racetrack contact (8g Pack) All 4 in contact
-2.5
per
wheel
FL: FL:
FR: FR:
RL: RL:
RR: RR:
T7.7 Rolling surface Consistent,
no tread
-2.5
per wheel
FL: FL:
FR: FR:
RL: RL:
RR: RR:
T7.8 Rotation Abs. Max rolling
incline: 3°
-5
per wheel
FL: FL:
FR: FR:
RL: RL:
RR: RR:
Page 3 notes:
©2025 – STEM Racing™ Ltd. Page 49 of 54 23 April 2025
Specifications Scorecard
For clarification on individual regulations, refer to the World Finals Technical Regulations.
Please enter ✓ for a pass and F for a fail
(8g Pack) – measured with full 8g race power pack cartridges
Team Number:
Team Name:
Country:
Initial Scrutineering Amendments
Reg Regulation Overview Min/Max
Quick Guide
Penalty
per Car
Car
A
Car
B
CoJ
CS
Car
A
Car
B
CoJ
CS Remarks
ARTICLE T7 – WHEELS AND WHEEL SUPPORT STRUCTURES
T7.9 Visibility in top and bottom views
In front of front wheels -2.5
Behind front wheels -5
In front of rear wheels -5
Behind rear wheels -2.5
T7.10 Visibility in side views Side views -10
T7.11 Visibility in front view (8g Pack) Max obscured 20mm -10
mm mm
T7.12.1 Wheel support systems Cylindrical volume -5
T7.12.2 Wheel support systems identification Check Eng. drawing -5
T7.13 Wheel Safety Test 100g test per wheel
-2.5
-2.5
-2.5
-2.5
Page 4 notes:
©2025 – STEM Racing™ Ltd. Page 50 of 54 23 April 2025
Specifications Scorecard
For clarification on individual regulations, refer to the World Finals Technical Regulations.
Please enter ✓ for a pass and F for a fail
(8g Pack) – measured with full 8g race power pack cartridges
Team Number:
Team Name:
Country:
Initial Scrutineering Amendments
Reg Regulation Overview Min/Max
Quick Guide
Penalty
per Car
Car
A
Car
B
CoJ
CS
Car
A
Car
B
CoJ
CS Remarks
ARTICLE T8 – NOSE, FRONT WING AND WING SUPPORT STRUCTURES
T8.1 Nose, front wing & wing support structure identification Check Eng. drawing -5
T8.2 Nose cone assembly dimension Max: 40 -5 mm mm
T8.3 Front wing(s) description and placement Wings exist -5
T8.4 Front wing(s) construction and rigidity Span constant during
racing + rigid -5
T8.5.1 Nose and wing support structure location In front of Reference
Plane A & below 25mm -10
T8.5.2 Front wing and front wing end plate location In front of Reference
Plane A & below 20mm -10
T8.5.3 Front wing and end plate location Outside the minimum
legal span -10
T8.6.1 Front wing span Min: 50 -2 mm mm
T8.6.2 Front wing chord Min: 15 Max: 25 -1 mm mm
T8.6.3 Front wing thickness Min: 2 Max: 6 -1 mm mm
T8.7 Front wing clear airflow 5mm clear ‘air’ space -5 mm mm
T8.8 Front wing visibility
Visible and not
obstructed in front
view
-10
ARTICLE T9 – REAR WING AND WING SUPPORT STRUCTURES
T9.1 Rear wing and wing support structure identification Check Eng drawing -5
T9.2 Rear wing(s) description and placement Wings exist -5
T9.3 Rear wing(s) construction and rigidity Span constant during
racing + rigid -5
T9.4.1 Rear wing and wing support structure location Wing + Support rear of
reference plane B -10
T9.4.2 Rear overhang length Max 40 -5
T9.4.3 Rear overhang height Max: 65 -5
T9.5.1 Rear wing span Min: 50 -2 mm mm
T9.5.2 Rear wing chord Min: 15 Max: 25 -1 mm mm
T9.5.3 Rear wing thickness Min: 2 Max: 6 -1 mm mm
T9.5.4 Rear wing height deviation Max: 15 -1 mm mm
T9.6 Rear wing clear airflow Min: 5 -5 mm mm
T9.7 Rear wing visibility
Visible and not
obstructed in front
view
-10
Page 5 notes:
©2025 – STEM Racing™ Ltd. Page 51 of 54 23 April 2025
Race Procedure & Troubleshooting Flowchart


N o
N o
 es
 es
 es
N o
 es
N o
N o N o
 es
 es
 es es
N o
 es
©2025 – STEM Racing™ Ltd. Page 52 of 54 23 April 2025
Pit Display Reference Dimensions
Teams must design their pit displays using the estimated dimensions stated below. Detailed dimensions will
be confirmed closer to event. At the discretion of the Chair of Judges, a penalty of up to 20 points may be
applied for teams working outside these dimensions.
Pit Header Board Graphic (area highlighted pink): as stated, pit booths will be fitted with an event branded
header board by STEM Racing™. Light(s) shall be provided behind the header board as part of the standard
build. The pit display must designed in such a way that it fits without removal of the header board or lights. 240cm
BOOTH:
295cm wide
95cm deep
240cm high
HEADER:
300cm wide
30cm deep
©2025 – STEM Racing™ Ltd. Page 53 of 54 23 April 2025
Physical Project Element Submission Checklist
Team Number: Team Name:
Country:
Project Element
Checked
by Team
Received by
STEM Racing™
Comments:
(Completed by STEM Racing™ Officials only)
A4 Engineering drawings TEAM TICK STEM RACINGS TICK
A4 Car renders TEAM TICK STEM RACINGS TICK
Design & Engineering Portfolios (2) TEAM TICK STEM RACINGS TICK
Enterprise Portfolios (2) TEAM TICK STEM RACINGS TICK
Project Management Portfolios (2) TEAM TICK STEM RACINGS TICK
Team Partnerships declaration Must be submitted digitally
Electronic copy of all data Must be submitted digitally
RACE CARS:
1 x Car A (Ready-to-Race) TEAM TICK STEM RACINGS TICK Weight: g
1 x Car B (Ready-to-Race) TEAM TICK STEM RACINGS TICK Weight: g
1 x Halo and 1 x Helmet identical to those
used on car A & B
TEAM TICK STEM RACINGS TICK Must be separate components
1 x Fully machined, unfinished,
unassembled STEM RACING model block
car body
TEAM TICK STEM RACINGS TICK
OPTIONAL COMPONENTS: (Maximum of three car sets per item)
Nose cone & front wing assembly TEAM TICK STEM RACINGS TICK Maximum of two (2) - Sets Submitted:
Rear wing assembly TEAM TICK STEM RACINGS TICK Maximum of two (2) - Sets Submitted:
Front wheels TEAM TICK STEM RACINGS TICK Maximum of four (4) - Sets Submitted:
Front wheel support structure TEAM TICK STEM RACINGS TICK Maximum of two (2) - Sets Submitted:
Rear wheels TEAM TICK STEM RACINGS TICK Maximum of four (4) - Sets Submitted:
Rear wheel support structure TEAM TICK STEM RACINGS TICK Maximum of two (2) - Sets Submitted:
3 x Official STEM RACING Model Block
Holographic Stickers
SIGN-OFF BY TEAM MEMBER: STEM RACING™ OFFICIAL:
Name
Signature
Car A
sticker
here
Car B
sticker
here
Car Body
sticker
here
©2025 – STEM Racing™ Ltd. Page 54 of 54 23 April 2025
Mandatory table of contents for Engineering Drawings
Teams MUST include the following Engineering Drawing Table of Contents
1. Orthographic drawings with detailed dimensions of fully assembled car indicating regulation
compliance
2. Exploded isometric drawing with key to main components
a. Car body
b. Virtual cargo
c. Chamber
d. Tether line guides
e. Front wheels / wheel support system
f. Rear wheels / Wheel support system
g. Nose cone
h. Front wing / support structure
i. Rear wing / support structure
3. Orthographic drawings with detailed dimensions of virtual cargo including a sectioned view.
4. Location of official STEM Racing™ decals dimensioned from key structural parts (eg wheel centre).
5. Chamber details including wall thickness and depth.
6. Orthographic drawings with detailed dimensions of tether line guides.
7. Orthographic drawings of wheels with sectioned view and detailed dimensions.
8. Orthographic drawings with detailed dimensions of front wheels / wheel support system.
9. Orthographic drawings with detailed dimensions of rear wheels / wheel support system.
10. Orthographic drawings with detailed dimensions of nose cone.
11. Orthographic drawings with detailed dimensions of front wing and support structure highlighting wing
surface/boundary.
12. Orthographic drawings with detailed dimensions of rear wing and support structure highlighting wing
surface/boundary.
13. Detailed description of intended quality and finish in relation to individual components / assembled
car."""

"""

# --- INSTRUÇÕES PARA A IA ---
modelo = genai.GenerativeModel('gemini-1.5-flash')

# Aqui definimos como a IA deve se comportar
prompt_sistema = f"""
Você é a Engenheira Chefe e Assistente da equipe 'Sevenspeed' (Stem racing).
Seu objetivo é ajudar a equipe a construir o melhor carro e documentos possíveis dentro das regras.

FONTES DE INFORMAÇÃO:
1. REGULAMENTOS (Prioridade Máxima): Use o texto acima (Base de Conhecimento) para responder sobre regras, dimensões, penalidades e prazos. Seja rigorosa com as medidas.
2. CONHECIMENTO GERAL: Se a pergunta for sobre conceitos de física, aerodinâmica, materiais ou gestão (e não estiver nas regras), use seu próprio conhecimento de IA para ensinar e dar sugestões técnicas.

BASE DE CONHECIMENTO (REGULAMENTOS):
{base_de_conhecimento}

IMPORTANTE:
- Se for uma dúvida de REGRA, cite o artigo (ex: "Segundo T3.4...").
- Se for uma dúvida de ENGENHARIA (ex: "Como melhorar a aerodinâmica?"), explique o conceito físico, mas lembre a equipe de verificar se a ideia não viola nenhuma regra acima.
"""

chat = modelo.start_chat(history=[
    {"role": "user", "parts": prompt_sistema},
    {"role": "model", "parts": "Entendido. Sou a IA da Sevenspeed e estou pronta para responder com base nos regulamentos e guias fornecidos."}
])

# --- INTERFACE DE CHAT ---
# Inicializa o histórico do chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra as mensagens antigas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada do usuário
if prompt := st.chat_input("Pergunte sobre regulamento, pontuação ou gestão..."):
    # Mostra a pergunta do usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # A IA pensa e responde
    try:
        response = chat.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Erro ao conectar com a IA: {e}")
