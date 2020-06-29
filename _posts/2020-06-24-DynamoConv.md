---
layout: post
title: "Building a Hub Dynamo USB-Charger"
date: 2020-6-24
usemathjax: true
---

## Idea

Wouldn't it be great to have your smartphone charged while driving your bike?
Even better, imagine to charge your smartphone while driving the bike without having to bring a powerbank?
Especially if you are using your phone as an aid to  navigation, you might have realized that the battery levels drop fast, so charging is really necessary if you are going on longer tours.

I thought the same and naturally started to search for products that might do this on the internet.
It turns out that there are quite a lot of chargers, but (at least for hub dynamos, like the one shown in Fig.1) they are ludicrously expensive.

{% include image.html url="/assets/HubDynamoExample.jpg" description="<b>Fig.1</b>: Example of a hub dynamo [CC-BY-SA 4.0, Oxensepp]" %}

Think like 200 - 300 bucks or something for electronics that probably don't cost more than probably 10 bucks (at least the way I built mine) in parts.
Now I don't want to say that those are rip-offs, they *are* a niche product, and naturally will have to raise prices, but I was convinced that I could do the same for way less.
And I was right as it turns out.

## The Plan

I thought that I could not have been the first to think of this idea, so I did some more digging on the internet and found out that I was right: [this wonderful blog post](https://parttimetinkerer.wordpress.com/2011/11/12/charging-usb-devices-from-a-hub-dynamo/) shows how to convert the AC-signal from a typical hub dynamo to a 5V DC signal, which might be used to charge a USB-Device.
Because the post there explains the whole process of choosing the electrical parts in great detail, I highly encourage you to read it if you want to find out more.
My only contribution was to change out the LM2940 regulator for a more modular part, namely the LM2596 step down converter, which can easily be sourced on [ebay](https://www.ebay.com/sch/i.html?&_nkw=lm2596) for a couple of bucks.
I also chose a modular full bridge rectifier circuit, which can also be easily found on ebay.

Building the circuit then is as simple as soldering four parts together: first the rectifier, then a 16V 2200 $$\mu$$f capacitor to smooth out the signal followed by the LM2596 buck converter which feeds into a usb port.
Fig.2 shows how the soldering was done on a prototyping board which was later cut to size.

{% include image.html url="/assets/Soldering.jpeg" description="<b>Fig.2</b>: Soldering the capacitor to the full bridge rectifier." %}

At every step in the process we tested the circuit with a simple multimeter.
First the rectifier-capacitor circuit was tested on its ability to create a dc signal from a arbitrary ac signal created by a lab power supply.
Next, after the buck converter was added, the stability of the 5V signal was tested.
Just as [the blog write up](https://parttimetinkerer.wordpress.com/2011/11/12/charging-usb-devices-from-a-hub-dynamo/) above stated, the addition of a large capacitor proved to be a good stabilizer and the circuit puts out 5V even for a low frequency of the hub dynamo.
Some part of the testing is shown in fig.3 .

{% include image.html url="/assets/Testing.jpeg" description="<b>Fig.3</b>: Testing the circuit after the addition of the DC-DC converter." %}

After the circuit had been rigorously tested, it was time to put a box around it in order for it to be shielded from the elements when driving.
To that end I designed a simple 3d-printable enclosure with two separate compartments.
One compartment for the bulk of the more sensitive components such as the capacitor and the converter, and the second one for the USB port.
Putting everything into the box, we sealed of the interface between the compartments with hot glue.
The reasoning behind this was that the box has to have a opening on one side to enable the smartphone to be plugged in, but we also did not want to have any chance of water getting inside the box with the more vulnerable parts.

Finally the box was fixed to my bike using some simple zip ties.
The end product is shown in fig. 4 .

{% include image.html url="/assets/Installation.jpeg" description="<b>Fig.3</b>: Installing the 3d printed box on the bike. Power from the dynamo was grabbed by soldering two small wires to the cables that originally were connected only to the main torch. The USB port is located on the underside of the small box." %}

Long term tests on the ability of the circuit to charge a phone still have to be carried out, although first tests showed that I was at least able to keep the battery at the same level for the duration of small (about 10km) tours.
The final constellation of a phone connected to the charger, while being supported by a 3d-printable phone holder located on the handlebar is shown in fig. 5.

{% include image.html url="/assets/Installation2.jpeg" description="<b>Fig.3</b>: Final setup of the charging circuit on my bike." %}
