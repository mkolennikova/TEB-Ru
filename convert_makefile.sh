#!/bin/bash

# Final script to convert Makefile:
# - keep explicit dependency rules, but remove compilation commands
# - add $(OBJDIR)/ prefix to targets and dependencies
# - remove all cp commands and localize rules
# - add generic compilation rules and vpath
# - add include and module flags to gfortran_args

set -e

MAKEFILE="Makefile"
BACKUP="${MAKEFILE}.bak"
OBJDIR="obj"

echo "=== Converting Makefile to build into $OBJDIR directory ==="

# 1. Backup
if [ -f "$MAKEFILE" ]; then
    cp "$MAKEFILE" "$BACKUP"
    echo "Backup created: $BACKUP"
else
    echo "Error: $MAKEFILE not found!"
    exit 1
fi

# 2. Remove old compilation command lines (starting with tab and $(FC))
sed -i '/^[[:space:]]*$(FC)/d' "$MAKEFILE"
echo "Removed old compilation commands."

# 3. Remove all cp commands (lines starting with tab and cp)
sed -i '/^[[:space:]]*cp /d' "$MAKEFILE"
echo "Removed all cp commands."

# 4. Remove localize target and its dependencies
sed -i '/^localize:/d' "$MAKEFILE"
sed -i '/^OFF = /d' "$MAKEFILE"
echo "Removed localize and OFF."

# 5. Add OBJDIR and mkdir after include
sed -i "/^include gfortran_args/a OBJDIR = $OBJDIR\n\$(shell mkdir -p \$(OBJDIR))" "$MAKEFILE"
echo "Added OBJDIR and mkdir."

# 6. Redefine OBJ list with prefix $(OBJDIR)/
sed -i 's/^OBJ = /OBJ = \$(addprefix \$(OBJDIR)\/, /' "$MAKEFILE"
sed -i '/^OBJ = \$(addprefix .*/ s/$/)/' "$MAKEFILE"
echo "Updated OBJ list with path to $OBJDIR."

# 7. Transform all rule targets and dependencies to include $(OBJDIR)/
sed -i '/:/s/ \([^ ]*\)\.o/ $(OBJDIR)\/\1.o/g; s/^\([^ ]*\)\.o:/$(OBJDIR)\/\1.o:/' "$MAKEFILE"
echo "Updated rule targets and dependencies to use $(OBJDIR)/."

# 8. Remove lines starting with './' (copy rules for localize)
sed -i '/^\.\//d' "$MAKEFILE"
echo "Removed localize copy rules."

# 9. Append generic build rules and vpath (fallback)
cat >> "$MAKEFILE" << 'EOF'

# ----- Generic rules for building into obj/ (fallback) -----
vpath %.F90 src_driver src_teb src_struct src_proxi_SVAT src_solar
vpath %.f90 src_driver src_teb src_struct src_proxi_SVAT src_solar
vpath %.F   src_teb
vpath %.f   src_teb

$(OBJDIR)/%.o: %.F90 | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.f90 | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.F | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@

$(OBJDIR)/%.o: %.f | $(OBJDIR)
	$(FC) $(CPPDEFS) $(CPPFLAGS) $(FFLAGS) $(OTHERFLAGS) -c $< -o $@
EOF

# 10. Fix driver1.exe rule
sed -i '/^driver1.exe:/c driver1.exe: $(OBJ) | $(OBJDIR)' "$MAKEFILE"
sed -i '/^driver1.exe:.*/a \\t$(LD) $(OBJ) -o driver1.exe $(LDFLAGS)' "$MAKEFILE"

# 11. Update clean: remove obj/ and all .mod files anywhere
sed -i '/^clean:/a \\t-rm -f $(shell find . -name "*.mod" 2>/dev/null)' "$MAKEFILE"
sed -i '/^clean:/a \\t-rm -rf $(OBJDIR)' "$MAKEFILE"

echo "Added generic compilation rules, fixed driver1.exe and clean."

# 12. Add include and module flags to gfortran_args
if grep -q "\-I. -Isrc_teb" gfortran_args; then
    echo "Include flags already present in gfortran_args."
else
    sed -i '/^FFLAGS = .*gfortran/s/$/ -I. -Isrc_teb/' gfortran_args
    sed -i '/^FFLAGS = .*ifort/s/$/ -I. -Isrc_teb/' gfortran_args
    echo "Added -I. -Isrc_teb to gfortran_args."
fi

if grep -q "\-J\$(OBJDIR)" gfortran_args; then
    echo "Module flag -J already present in gfortran_args."
else
    sed -i '/^FFLAGS = .*gfortran/s/$/ -J$(OBJDIR)/' gfortran_args
    echo "Added -J$(OBJDIR) to gfortran_args for gfortran."
fi

if grep -q "\-module \$(OBJDIR)" gfortran_args; then
    echo "Module flag -module already present in gfortran_args."
else
    sed -i '/^FFLAGS = .*ifort/s/$/ -module $(OBJDIR)/' gfortran_args
    echo "Added -module $(OBJDIR) to gfortran_args for ifort."
fi

echo "=== Conversion completed! ==="
echo "Run 'make clean && make' to build."
echo "Backup: $BACKUP"