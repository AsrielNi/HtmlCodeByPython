from src import *


with HtmlDocument() as doc:
    with HtmlHead(parent_container=doc) as head:
        pass
    with HtmlBody(parent_container=doc) as body:
        body.attach(HtmlHeading("title_1", "Title Example"))
        body.attach(HtmlParagraph("paragraph_1", "I'm Paragraph 1 ~~~~"))
        with HtmlDivision("div1", parent_container=body) as div1:
            div1.attach(HtmlParagraph("paragraph_2", "Test div. In div1"))
            div1.attach(
                HtmlParagraph("paragraph_3", "Span for this paragraph").text_modify(
                    HtmlSpan("Test_span").set_global_attr({"style": "color:#f00;"})))
        with HtmlDivision("div2", parent_container=body) as div2:
            div2.attach(HtmlParagraph("paragraph_4", "Test Form"))
            with HtmlForm("Form1", parent_container=div2) as form1:
                with HtmlParagraph("p_test", parent_container=form1) as p_test:
                    p_test.attach(HtmlInput("input_name").set_individual_attr({"value": "your name"}))
                form1.attach(HtmlInput("input_password").set_individual_attr({"value": "your password"}))
                form1.attach(HtmlInput("submit_form", HtmlInput.InputType.SUBMIT).set_individual_attr({"value": "submit"}))

doc.build(".")