+++
title = "Ablation"
summary = "Removing a model component on purpose to measure how much it mattered — the standard “ablation study.”"
category = "Core concepts"
related = ["machine-learning", "val-loss", "parameters"]
+++
**Ablation** is the practice of removing a piece of a model or its training setup on purpose,
just to see how much that piece mattered. The word is borrowed from surgery, where it means
cutting away tissue — and the method is about that clinical: if you suspect some component is
doing real work, take it out, run the model again, and measure how much worse it gets. That
drop — or the lack of one — is your answer. A big drop means the part was load-bearing; no
change means it was decoration. The standard form is the **ablation study**, the table near the
end of nearly every [machine learning](/glossary/machine-learning/) paper where the authors knock out one ingredient at a
time — an attention head, a layer, a loss term, a slice of training data, a preprocessing step
— and report what the score did. It's how a field that can't fully open the black box still
reasons about cause: not by explaining _why_ a part helps, but by proving _that_ it does, one
amputation at a time. The thing you measure after each cut is usually a held-out metric like
[validation loss](/glossary/val-loss/), and the component you're pulling is often a bundle of [parameters](/glossary/parameters/) you're
betting the model can live without. Done well, it separates the parts that earn their keep from
the ones that just came along for the ride. Done lazily — yanking several things at once — it
tells you nothing, because you can't say which cut caused the bleeding.
