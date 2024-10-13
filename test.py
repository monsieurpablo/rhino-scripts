import Rhino
import Eto.Forms as forms
import Eto.Drawing as drawing
import scriptcontext as sc

class AssignUserTextDialog(forms.Form):
    def __init__(self):
        self.Title = 'Assign User Text'
        self.Padding = drawing.Padding(10)
        self.Resizable = True

        # Drop-down list for selecting a key
        self.dropdown = forms.DropDown()
        self.dropdown.DataStore = ['Material', 'Layer', 'Color']  # Add your options here
        self.dropdown.SelectedIndex = 0

        # Text box for inputting a value
        self.text_input = forms.TextBox(Text='')

        # Number input (for numeric user text)
        self.number_input = forms.NumericUpDown()
        self.number_input.DecimalPlaces = 2
        self.number_input.Value = 0.0  # Default value

        # OK and Cancel buttons
        self.ok_button = forms.Button(Text='Assign')
        self.ok_button.Click += self.OnOKButtonClick

        self.close_button = forms.Button(Text='Close')
        self.close_button.Click += self.OnCloseButtonClick

        # Layout
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        layout.AddRow('Select Key:', self.dropdown)
        layout.AddRow('Text Input:', self.text_input)
        layout.AddRow('Number Input:', self.number_input)
        layout.AddRow(None)  # Spacer
        layout.AddRow(self.ok_button, self.close_button)

        self.Content = layout

    # Handler for OK button click
    def OnOKButtonClick(self, sender, e):
        selected_key = self.dropdown.SelectedValue
        text_value = self.text_input.Text
        numeric_value = self.number_input.Value

        # Get user to select a surface
        rc, obj_ref = Rhino.Input.RhinoGet.GetOneObject(
            "Select a planar surface", False, Rhino.DocObjects.ObjectType.Surface)

        if rc == Rhino.Commands.Result.Success and obj_ref is not None:
            # Set the user text based on selected key and inputs
            rhino_object = obj_ref.Object()
            value_to_assign = text_value if text_value else str(numeric_value)
            rhino_object.Attributes.SetUserString(selected_key, value_to_assign)
            rhino_object.CommitChanges()
            Rhino.RhinoApp.WriteLine(
                "Assigned {0}: {1} to surface.".format(selected_key, value_to_assign))
        else:
            Rhino.RhinoApp.WriteLine("No surface selected or operation canceled.")

    # Handler for Close button click
    def OnCloseButtonClick(self, sender, e):
        self.Close()

def show_dialog():
    dialog = AssignUserTextDialog()
    dialog.Owner = Rhino.UI.RhinoEtoApp.MainWindow
    dialog.Show()  # Use Show() for modeless dialog

show_dialog()
